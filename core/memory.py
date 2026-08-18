import aiosqlite
import asyncio
from datetime import datetime

DB_PATH = "automaton.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                thought TEXT,
                action TEXT,
                result TEXT,
                success INTEGER
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                description TEXT,
                amount_usd REAL,
                balance REAL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS state (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        await db.commit()

async def log_action(thought: str, action: str, result: str, success: bool):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO actions (timestamp, thought, action, result, success) VALUES (?,?,?,?,?)",
            (datetime.now().isoformat(), thought, action, result, int(success))
        )
        await db.commit()

async def log_earning(description: str, amount: float):
    balance = await get_balance()
    new_balance = balance + amount
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO ledger (timestamp, description, amount_usd, balance) VALUES (?,?,?,?)",
            (datetime.now().isoformat(), description, amount, new_balance)
        )
        await db.commit()
    return new_balance

async def get_balance() -> float:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT balance FROM ledger ORDER BY id DESC LIMIT 1") as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0.0

async def set_state(key: str, value: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO state (key, value) VALUES (?,?)",
            (key, value)
        )
        await db.commit()

async def get_state(key: str) -> str | None:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT value FROM state WHERE key=?", (key,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

async def recent_actions(limit: int = 10) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT timestamp, thought, action, result, success FROM actions ORDER BY id DESC LIMIT ?",
            (limit,)
        ) as cursor:
            return await cursor.fetchall()
