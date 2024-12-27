import sqlite3
from typing import Generator

from app.core.config import settings


def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(settings.SPEAKERS_DB, check_same_thread=False)  # 允许多线程共享
    try:
        yield conn
    finally:
        conn.close()
