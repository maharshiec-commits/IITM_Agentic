from __future__ import annotations
import json, sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

DEFAULT_DB_PATH = "data/memory.db"

def _utc() -> str:
    return datetime.utcnow().isoformat()

@dataclass
class MemoryItem:
    key: str
    value: Any
    confidence: float = 1.0

class MemoryStore:
    def __init__(self, db_path: str = DEFAULT_DB_PATH) -> None:
        self.db_path = db_path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        con = self._connect()
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_memory (
            user_id TEXT NOT NULL,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            confidence REAL NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY (user_id, key)
        )""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS case_memory (
            case_id TEXT NOT NULL,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY (case_id, key)
        )""")
        con.commit()
        con.close()

    def upsert_user_memory(self, user_id: str, item: MemoryItem) -> None:
        con = self._connect()
        cur = con.cursor()
        cur.execute("""
        INSERT INTO user_memory(user_id, key, value, confidence, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id, key) DO UPDATE SET
            value=excluded.value,
            confidence=excluded.confidence,
            updated_at=excluded.updated_at
        """, (user_id, item.key, json.dumps(item.value), float(item.confidence), _utc()))
        con.commit(); con.close()

    def get_user_memory(self, user_id: str) -> Dict[str, Any]:
        con = self._connect(); cur = con.cursor()
        cur.execute("SELECT key, value FROM user_memory WHERE user_id=?", (user_id,))
        rows = cur.fetchall(); con.close()
        return {k: json.loads(v) for (k, v) in rows}

    def upsert_case_memory(self, case_id: str, key: str, value: Any) -> None:
        con = self._connect(); cur = con.cursor()
        cur.execute("""
        INSERT INTO case_memory(case_id, key, value, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(case_id, key) DO UPDATE SET
            value=excluded.value,
            updated_at=excluded.updated_at
        """, (case_id, key, json.dumps(value), _utc()))
        con.commit(); con.close()

    def get_case_memory(self, case_id: str) -> Dict[str, Any]:
        con = self._connect(); cur = con.cursor()
        cur.execute("SELECT key, value FROM case_memory WHERE case_id=?", (case_id,))
        rows = cur.fetchall(); con.close()
        return {k: json.loads(v) for (k, v) in rows}
