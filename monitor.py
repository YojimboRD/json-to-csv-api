import asyncio
import aiohttp
import time
from datetime import datetime

GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

API_URL = "http://127.0.0.1:5000"

async def get_eur_rate() -> float:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://open.er-api.com/v6/latest/USD") as resp:
                data = await resp.json()
                return data["rates"]["EUR"]
    except Exception:
        return 0.92

async def monitor():
    print(f"{GREEN}Starting API Monitor...{RESET}")
    print(GREEN + "-" * 60 + RESET)

    eur_rate = await get_eur_rate()
    last_request_count = 0
    tick = 0

    while True:
        tick += 1
        now = datetime.now().strftime('%H:%M:%S')

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{API_URL}/earnings") as resp:
                    data = await resp.json()
                    total_usd = data.get("total_earnings_usd", 0.0)
                    total_requests = data.get("total_requests", 0)
                    entries = data.get("entries", [])
                    eur_balance = round(total_usd * eur_rate, 4)

                    print(f"\n{GREEN}[{now}] Tick #{tick} | Balance: €{eur_balance:.4f} | Requests: {total_requests}{RESET}")

                    if total_requests > last_request_count:
                        new = total_requests - last_request_count
                        latest = entries[-1] if entries else {}
                        earned = round(new * 0.01 * eur_rate, 4)
                        print(f"  {YELLOW}NEW REQUEST{RESET} +{new} request(s) | +€{earned:.4f} earned")
                        print(f"  {CYAN}LAST: {latest.get('timestamp','?')} | rows={latest.get('rows_converted','?')} | €{round(0.01 * eur_rate, 4):.4f}{RESET}")
                        last_request_count = total_requests
                    else:
                        print(f"  STATUS:  API live, waiting for requests...")

        except Exception as e:
            print(f"\n{GREEN}[{now}] Tick #{tick}{RESET}")
            print(f"  ERROR: API unreachable — {e}")

        await asyncio.sleep(15)

if __name__ == "__main__":
    try:
        asyncio.run(monitor())
    except KeyboardInterrupt:
        print("\n[STOPPED] Monitor shut down.")
