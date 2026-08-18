import asyncio
import aiohttp
from core.memory import log_earning, get_balance

async def get_eur_rate() -> float:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://open.er-api.com/v6/latest/USD") as resp:
                data = await resp.json()
                return data["rates"]["EUR"]
    except Exception:
        return 0.92

async def sync_from_api(api_url: str = "http://127.0.0.1:5000"):
    try:
        eur_rate = await get_eur_rate()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{api_url}/earnings") as resp:
                data = await resp.json()
                entries = data.get("entries", [])
                total_api = data.get("total_earnings_usd", 0.0)
                current_balance = await get_balance()
                if total_api > current_balance:
                    diff = round(total_api - current_balance, 4)
                    new_balance = await log_earning(
                        f"API earnings sync ({len(entries)} requests)", diff
                    )
                    eur_balance = round(new_balance * eur_rate, 4)
                    eur_diff = round(diff * eur_rate, 4)
                    print(f"[SYNC] +€{eur_diff:.4f} -> Balance: €{eur_balance:.4f} [rate: {eur_rate:.4f}]")
                else:
                    eur_balance = round(current_balance * eur_rate, 4)
                    print(f"[SYNC] Up to date: €{eur_balance:.4f} [rate: {eur_rate:.4f}]")
    except Exception as e:
        print(f"[SYNC] Failed: {e}")

if __name__ == "__main__":
    asyncio.run(sync_from_api())
