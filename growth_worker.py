import asyncio
import aiohttp
from datetime import datetime
import json
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
DIM    = "\033[2m"
RESET  = "\033[0m"

GITHUB_REPO = "https://github.com/YojimboRD/json-to-csv-api"
API_URL = "http://127.0.0.1:5000"
CHECK_INTERVAL = 3600  # check every hour

SYSTEM_PROMPT = """You are a Growth Worker agent. Your only job is to monitor and grow traffic to a JSON to CSV API.

You have access to:
- Current request count and earnings
- List of promotion channels already used
- Ability to suggest new promotion actions

Respond with valid JSON only:
{
  "thought": "one short sentence",
  "action": "monitor|suggest_promotion|update_github",
  "details": "specific details about the action"
}

Keep responses under 300 characters total."""

async def get_stats() -> dict:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/earnings") as resp:
                data = await resp.json()
                return {
                    "total_requests": data.get("total_requests", 0),
                    "total_earnings_usd": data.get("total_earnings_usd", 0)
                }
    except:
        return {"total_requests": 0, "total_earnings_usd": 0}

async def think(stats: dict, last_stats: dict) -> dict:
    new_requests = stats["total_requests"] - last_stats.get("total_requests", 0)
    
    prompt = f"""Current stats:
- Total requests: {stats['total_requests']}
- New requests since last check: {new_requests}
- Total earned: ${stats['total_earnings_usd']:.2f}
- GitHub repo: {GITHUB_REPO}
- Dev.to posts: 3 published
- Channels tried: Dev.to, GitHub

What should I do to grow traffic?"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    try:
        return json.loads(raw)
    except:
        return {"thought": "parse error", "action": "monitor", "details": ""}

async def run():
    print(f"{GREEN}[GROWTH WORKER] Starting...{RESET}")
    print(f"{GREEN}[GROWTH WORKER] Monitoring every {CHECK_INTERVAL//60} minutes{RESET}")
    print(GREEN + "-" * 60 + RESET)

    last_stats = await get_stats()
    tick = 0

    while True:
        tick += 1
        now = datetime.now().strftime('%H:%M:%S')
        stats = await get_stats()
        new_requests = stats["total_requests"] - last_stats.get("total_requests", 0)

        print(f"\n{GREEN}[{now}] Growth Tick #{tick}{RESET}")
        print(f"  Requests: {stats['total_requests']} (+{new_requests} new)")
        print(f"  Earnings: ${stats['total_earnings_usd']:.2f}")

        if new_requests > 0:
            print(f"  {CYAN}🎉 {new_requests} new request(s) since last check!{RESET}")

        decision = await think(stats, last_stats)
        print(f"  THOUGHT: {decision.get('thought', '')}")
        print(f"  ACTION:  {decision.get('action', '')}")
        print(f"  DETAILS: {decision.get('details', '')}")

        last_stats = stats
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\n[GROWTH WORKER] Stopped.")
