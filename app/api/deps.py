import sqlite3
from typing import Generator


def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect("speakers.db", check_same_thread=False)  # 允许多线程共享
    try:
        yield conn
    finally:
        conn.close()
