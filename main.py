import asyncio
import sys
from core.agent import run_loop

if __name__ == "__main__":
    try:
        asyncio.run(run_loop())
    except KeyboardInterrupt:
        print("\n[STOPPED] Automaton shut down by user.")
        sys.exit(0)
