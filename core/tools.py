import asyncio
import aiohttp
import os
import subprocess
from pathlib import Path

WORKSPACE = Path("workspace")
WORKSPACE.mkdir(exist_ok=True)

# Hard limits - these cannot be overridden by the agent
BLOCKED_COMMANDS = [
    "rm -rf /", "mkfs", "dd if=", ":(){:|:&};:",
    "shutdown", "reboot", "halt"
]

def is_safe_command(cmd: str) -> bool:
    cmd_lower = cmd.lower()
    for blocked in BLOCKED_COMMANDS:
        if blocked in cmd_lower:
            return False
    return True

async def run_shell(command: str) -> dict:
    if not is_safe_command(command):
        return {"success": False, "output": "BLOCKED: command not permitted by constitution"}
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True,
            text=True, timeout=30, cwd=str(WORKSPACE)
        )
        output = result.stdout + result.stderr
        return {"success": result.returncode == 0, "output": output[:2000]}
    except subprocess.TimeoutExpired:
        return {"success": False, "output": "ERROR: command timed out after 30s"}
    except Exception as e:
        return {"success": False, "output": f"ERROR: {str(e)}"}

async def read_file(path: str) -> dict:
    try:
        full_path = WORKSPACE / path
        if not full_path.resolve().is_relative_to(WORKSPACE.resolve()):
            return {"success": False, "output": "BLOCKED: cannot read outside workspace"}
        content = full_path.read_text()
        return {"success": True, "output": content[:5000]}
    except Exception as e:
        return {"success": False, "output": f"ERROR: {str(e)}"}

async def write_file(path: str, content: str) -> dict:
    try:
        full_path = WORKSPACE / path
        if not full_path.resolve().is_relative_to(WORKSPACE.resolve()):
            return {"success": False, "output": "BLOCKED: cannot write outside workspace"}
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
        return {"success": True, "output": f"Written {len(content)} bytes to {path}"}
    except Exception as e:
        return {"success": False, "output": f"ERROR: {str(e)}"}

async def web_get(url: str) -> dict:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                text = await resp.text()
                return {"success": True, "output": text[:3000], "status": resp.status}
    except Exception as e:
        return {"success": False, "output": f"ERROR: {str(e)}"}

async def list_workspace() -> dict:
    try:
        files = []
        for f in WORKSPACE.rglob("*"):
            if f.is_file():
                files.append(str(f.relative_to(WORKSPACE)))
        return {"success": True, "output": "\n".join(files) if files else "(empty)"}
    except Exception as e:
        return {"success": False, "output": f"ERROR: {str(e)}"}

TOOL_MAP = {
    "shell": run_shell,
    "read_file": read_file,
    "write_file": write_file,
    "web_get": web_get,
    "list_workspace": list_workspace,
}

async def execute_tool(tool_name: str, **kwargs) -> dict:
    if tool_name not in TOOL_MAP:
        return {"success": False, "output": f"Unknown tool: {tool_name}"}
    return await TOOL_MAP[tool_name](**kwargs)
