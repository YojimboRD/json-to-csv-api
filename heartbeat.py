import asyncio
import aiohttp
from datetime import datetime
from core.memory import get_balance
from core.sync_earnings import sync_from_api, get_eur_rate

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

async def check_tunnel(url: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                return resp.status == 200
    except:
        return False

async def heartbeat():
    print(f"{GREEN}[HEARTBEAT] Starting...{RESET}")
    eur_rate = await get_eur_rate()
    tunnel_url = "https://seating-stephanie-assurance-participate.trycloudflare.com"

    while True:
        now = datetime.now().strftime('%H:%M:%S')
        await sync_from_api()
        balance = await get_balance()
        eur_balance = round(balance * eur_rate, 4)

        tunnel_ok = await check_tunnel(tunnel_url)
        tunnel_status = f"{GREEN}UP{RESET}" if tunnel_ok else f"{RED}DOWN{RESET}"

        if eur_balance >= 0.50:
            mode = f"{GREEN}NORMAL{RESET}"
        elif eur_balance >= 0.20:
            mode = f"{YELLOW}LOW{RESET}"
        elif eur_balance >= 0.05:
            mode = f"{YELLOW}CRITICAL{RESET}"
        else:
            mode = f"{RED}DEAD{RESET}"

        print(f"[{now}] HEARTBEAT | Balance: €{eur_balance:.4f} | Mode: {mode} | Tunnel: {tunnel_status}")

        await asyncio.sleep(300)

if __name__ == "__main__":
    try:
        asyncio.run(heartbeat())
    except KeyboardInterrupt:
        print("\n[HEARTBEAT] Stopped.")
