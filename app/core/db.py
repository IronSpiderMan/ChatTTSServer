import sqlite3

from app.core.config import settings


def init_db():
    with sqlite3.connect(settings.SPEAKERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS speakers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            filepath TEXT NOT NULL
        )
        ''')
        conn.commit()
