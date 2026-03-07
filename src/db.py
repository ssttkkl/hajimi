import json
import time
import aiosqlite
from pathlib import Path

class SessionDB:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    async def init(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    task_id TEXT PRIMARY KEY,
                    metadata TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL
                )
            """)
            await db.commit()

    async def save(self, task_id: str, metadata: list):
        async with aiosqlite.connect(self.db_path) as db:
            now = time.time()
            await db.execute(
                "INSERT OR REPLACE INTO sessions (task_id, metadata, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (task_id, json.dumps(metadata), now, now)
            )
            await db.commit()

    async def load(self, task_id: str):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT metadata FROM sessions WHERE task_id = ?", (task_id,)) as cursor:
                row = await cursor.fetchone()
                return json.loads(row[0]) if row else None

    async def list_all(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT task_id, metadata FROM sessions") as cursor:
                rows = await cursor.fetchall()
                return [{"id": r[0], "cid": json.loads(r[1])[0] if r[1] else None} for r in rows]

    async def delete(self, task_id: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM sessions WHERE task_id = ?", (task_id,))
            await db.commit()
