import sqlite3
from sqlite3 import Connection
from typing import List

from fastapi import HTTPException

from app.models.chattts import Speaker, SpeakerPublic, SpeakerCreate


def read_speaker_by_name(db: Connection, name: str) -> Speaker:
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM speakers WHERE name='{name}'")
    if spk := cursor.fetchone():
        sid, name, filepath = spk
        return SpeakerPublic(id=sid, name=name, filepath=filepath)
    raise HTTPException(status_code=404, detail="Speaker not found")


def read_all_speakers(db: Connection) -> List[SpeakerPublic]:
    cursor = db.cursor()
    cursor.execute("SELECT id, name, filepath FROM speakers")
    spks = cursor.fetchall()
    speakers = []
    for spk in spks:
        sid, name, filepath = spk
        speakers.append(SpeakerPublic(id=int(sid), name=name, filepath=filepath))
    return speakers


def read_count_speakers(db: Connection) -> int:
    cursor = db.cursor()
    cursor.execute("SELECT count(*) FROM speakers")
    return cursor.fetchone()[0]


def create_speaker(db: Connection, speaker: SpeakerCreate, filepath: str) -> int:
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO speakers (name, filepath) VALUES (?, ?)",
            (speaker.name, filepath)
        )
        db.commit()
    except (sqlite3.InternalError, Exception) as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create speaker: {e}")
    finally:
        cursor.close()
    return 1


def delete_speaker_by_id(db: Connection, speaker_id: int) -> int:
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM speakers WHERE id = ?", (speaker_id,))
        if cursor.rowcount == 0:
            return 0
        db.commit()
        return 1
    except (sqlite3.InternalError, Exception) as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete speaker: {e}")
    finally:
        cursor.close()
