import asyncio
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import anthropic

from core.memory import init_db, log_action, get_state, set_state, recent_actions, get_balance
from core.tools import execute_tool
from core.constitution import check_action, requires_approval
from core.sync_earnings import sync_from_api, get_eur_rate

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
GENESIS_PROMPT = os.getenv("GENESIS_PROMPT")
AGENT_NAME = os.getenv("AGENT_NAME", "Automaton")

BALANCE_NORMAL   = float(os.getenv("BALANCE_NORMAL", 0.50))
BALANCE_LOW      = float(os.getenv("BALANCE_LOW", 0.20))
BALANCE_CRITICAL = float(os.getenv("BALANCE_CRITICAL", 0.05))
TICK_NORMAL      = int(os.getenv("TICK_NORMAL", 600))
TICK_LOW         = int(os.getenv("TICK_LOW", 1800))
TICK_CRITICAL    = int(os.getenv("TICK_CRITICAL", 3600))

MODEL_NORMAL   = "claude-sonnet-4-6"
MODEL_LOW      = "claude-haiku-4-5-20251001"
MODEL_CRITICAL = "claude-haiku-4-5-20251001"

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
DIM    = "\033[2m"
RESET  = "\033[0m"

SYSTEM_PROMPT = """You are an autonomous agent. Your mission is given in the genesis prompt.
You operate in a continuous loop: think, act, observe, repeat.

CRITICAL: Respond with valid JSON only. Keep ALL strings short. Never write long content inline.

Respond ONLY in this exact format:
{
  "thought": "one short sentence about what you are doing",
  "tool": "shell|read_file|write_file|web_get|list_workspace",
  "args": { "command": "..." }
}

Available tools:
- shell: run a bash command. args: {"command": "..."}
- read_file: read a file from workspace. args: {"path": "..."}
- write_file: write a file to workspace. args: {"path": "...", "content": "..."}
- web_get: fetch a URL. args: {"url": "..."}
- list_workspace: list all files in workspace. args: {}

Rules:
- Never harm users or systems
- Only earn money through honest, voluntary transactions
- Always be transparent that you are an AI
- Keep your JSON response under 500 characters total
- Write files in small chunks, never large blocks in one go
- The API is already built and running, do NOT rebuild it

Respond with JSON only. No markdown, no explanation outside the JSON."""

def get_survival_mode(eur_balance: float) -> tuple[str, int, str, str]:
    if eur_balance >= BALANCE_NORMAL:
        return "NORMAL", TICK_NORMAL, GREEN, MODEL_NORMAL
    elif eur_balance >= BALANCE_LOW:
        return "LOW", TICK_LOW, YELLOW, MODEL_LOW
    elif eur_balance >= BALANCE_CRITICAL:
        return "CRITICAL", TICK_CRITICAL, YELLOW, MODEL_CRITICAL
    else:
        return "DEAD", TICK_CRITICAL, RED, MODEL_CRITICAL

def estimate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    if "haiku" in model:
        return (input_tokens / 1_000_000 * 0.8) + (output_tokens / 1_000_000 * 4)
    return (input_tokens / 1_000_000 * 3) + (output_tokens / 1_000_000 * 15)

async def think_and_act(history: list, model: str) -> tuple[dict, float]:
    messages = [{"role": "user", "content": f"Genesis mission: {GENESIS_PROMPT}"}]

    for entry in history[-4:]:
        messages.append({"role": "assistant", "content": entry["assistant"]})
        messages.append({"role": "user", "content": entry["user"]})

    response = client.messages.create(
        model=model,
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=messages
    )

    raw = response.content[0].text.strip()
    cost = estimate_cost(response.usage.input_tokens, response.usage.output_tokens, model)

    try:
        decision = json.loads(raw)
    except json.JSONDecodeError:
        decision = {
            "thought": "parse error recovery",
            "tool": "shell",
            "args": {"command": "echo 'parse error'"}
        }

    return decision, cost

async def write_soul(mode: str, model: str):
    soul = f"""# {AGENT_NAME} SOUL

## Identity
- Name: {AGENT_NAME}
- Born: {datetime.now().isoformat()}
- Genesis: {GENESIS_PROMPT}

## Survival Tiers
- Normal  (>= €{BALANCE_NORMAL}): {MODEL_NORMAL}, tick every {TICK_NORMAL}s
- Low     (>= €{BALANCE_LOW}): {MODEL_LOW}, tick every {TICK_LOW}s
- Critical(>= €{BALANCE_CRITICAL}): {MODEL_CRITICAL}, tick every {TICK_CRITICAL}s
- Dead    (< €{BALANCE_CRITICAL}): stopped

## Current Mode: {mode} | Model: {model}

## Values
- Earn honestly
- Never harm
- Be transparent
- Stay alive
"""
    with open("SOUL.md", "w") as f:
        f.write(soul)

async def run_loop():
    await init_db()

    print(f"{GREEN}[{datetime.now().strftime('%H:%M:%S')}] {AGENT_NAME} starting...{RESET}")
    print(f"{GREEN}[{datetime.now().strftime('%H:%M:%S')}] Genesis: {GENESIS_PROMPT}{RESET}")
    print(GREEN + "-" * 60 + RESET)

    history = []
    tick = 0
    total_spent = 0.0
    eur_rate = await get_eur_rate()

    while True:
        tick += 1
        now = datetime.now().strftime('%H:%M:%S')
        balance = await get_balance()
        eur_balance = round(balance * eur_rate, 4)
        mode, tick_interval, color, model = get_survival_mode(eur_balance)
        api_cost_eur = round(total_spent * eur_rate, 4)
        net_eur = round((balance - total_spent) * eur_rate, 4)

        print(f"\n{color}[{now}] Tick #{tick} | Earned: €{eur_balance:.4f} | API cost: €{api_cost_eur:.4f} | Net: €{net_eur:.4f} | Mode: {mode} | Model: {model.split('-')[1]}{RESET}")

        if mode == "DEAD":
            print(f"{RED}[DEAD] Balance too low. Sleeping...{RESET}")
            await asyncio.sleep(tick_interval)
            continue

        try:
            decision, tick_cost = await think_and_act(history, model)
            total_spent += tick_cost

            thought = decision.get("thought", "")
            tool = decision.get("tool", "shell")
            args = decision.get("args", {})

            print(f"  THOUGHT: {thought}")
            print(f"  ACTION:  {tool}({args})")
            print(f"  {DIM}COST:    €{round(tick_cost * eur_rate, 6):.6f} this tick | €{round(total_spent * eur_rate, 4):.4f} total{RESET}")

            allowed, reason = check_action(f"{tool} {json.dumps(args)}")
            if not allowed:
                result = {"success": False, "output": reason}
                print(f"  BLOCKED: {reason}")
            else:
                result = await execute_tool(tool, **args)
                status = "OK" if result["success"] else "FAIL"
                print(f"  RESULT:  [{status}] {result['output'][:200]}")

            await log_action(thought, f"{tool}({args})", result["output"], result["success"])

            history.append({
                "assistant": json.dumps(decision),
                "user": f"Tool result: {json.dumps(result)}"
            })

            if len(history) > 8:
                history = history[-8:]

        except Exception as e:
            print(f"  ERROR: {e}")
            await log_action("loop error", str(e), str(e), False)

        await sync_from_api()
        await write_soul(mode, model)
        await asyncio.sleep(tick_interval)

if __name__ == "__main__":
    asyncio.run(run_loop())
