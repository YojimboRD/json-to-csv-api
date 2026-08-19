import sqlite3
import secrets
import os
from functools import wraps
from flask import request, jsonify

DB_PATH = os.getenv("API_KEYS_DB", "api_keys.db")


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                key         TEXT PRIMARY KEY,
                credits     INTEGER NOT NULL DEFAULT 0,
                used        INTEGER NOT NULL DEFAULT 0,
                stripe_session TEXT,
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def create_api_key(credits: int = 100, stripe_session: str = None) -> str:
    key = "atl_" + secrets.token_urlsafe(32)
    with _get_conn() as conn:
        conn.execute(
            "INSERT INTO api_keys (key, credits, stripe_session) VALUES (?, ?, ?)",
            (key, credits, stripe_session),
        )
        conn.commit()
    return key


def get_key_info(key: str):
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT key, credits, used, created_at FROM api_keys WHERE key = ?", (key,)
        ).fetchone()
    return dict(row) if row else None


def deduct_credit(key: str) -> bool:
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT credits FROM api_keys WHERE key = ?", (key,)
        ).fetchone()
        if not row or row["credits"] <= 0:
            return False
        conn.execute(
            "UPDATE api_keys SET credits = credits - 1, used = used + 1 WHERE key = ?",
            (key,),
        )
        conn.commit()
    return True


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-Key")
        if not key:
            return jsonify({"error": "Missing X-API-Key header"}), 401
        if not deduct_credit(key):
            info = get_key_info(key)
            if info is None:
                return jsonify({"error": "Invalid API key"}), 403
            return jsonify({"error": "No credits remaining. Visit /buy to top up."}), 402
        return f(*args, **kwargs)
    return decorated
