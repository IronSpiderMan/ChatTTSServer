import os
import io
import shutil
import asyncio
import sqlite3
from uuid import uuid4

import torch
from fastapi import APIRouter, HTTPException, Response, UploadFile, File
from fastapi.params import Depends

from app.api.deps import get_db
from app.core.config import settings
from app.utils import _tts
import app.globals as globals_
from app.models.chattts import Text, SpeakerCreate, SpeakersPublic
import app.cruds.chattts as chattts_cruds

router = APIRouter()


@router.post('/create-speaker')
async def create_speaker(
        file: UploadFile = File(...),
        speaker: SpeakerCreate = Depends(),
        session: sqlite3.Connection = Depends(get_db)
):
    # 保存上传的文件
    file_path = f"{settings.SPEAKERS_DIR}/{file.filename}"

    try:
        # 确保上传目录存在
        os.makedirs(settings.SPEAKERS_DIR, exist_ok=True)
        # 保存文件到本地
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    # 插入数据库记录
    if chattts_cruds.create_speaker(session, speaker, file_path):
        return {"message": "Speaker created successfully!", "speaker": speaker.name, "file_path": file_path}


@router.post("/sample-speaker")
async def sample_speaker():
    buffer = io.BytesIO()
    # 生成随机 speaker
    rand_spk = globals_.chattts.sample_random_speaker()
    # 保存文件到io
    torch.save(rand_spk, buffer)
    return Response(
        content=buffer.getvalue(),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={uuid4().hex}.pth"}
    )


@router.get('/list-speakers')
async def list_speakers(session: sqlite3.Connection = Depends(get_db)):
    spks = chattts_cruds.read_all_speakers(session)
    count = chattts_cruds.read_count_speakers(session)
    return SpeakersPublic(
        data=spks,
        count=count
    )


@router.post("/tts")
async def tts(text: Text, session: sqlite3.Connection = Depends(get_db)):
    if not text.text.strip():
        raise HTTPException(status_code=400, detail="Empty text")
    if text.speaker:
        speaker = chattts_cruds.read_speaker_by_name(session, text.speaker)
        content = await asyncio.to_thread(
            _tts,
            text=text.text,
            chattts=globals_.chattts,
            speaker_filepath=speaker.filepath
        )
    else:
        content = await asyncio.to_thread(_tts, text=text.text, chattts=globals_.chattts, speaker_filepath=None)
    return Response(
        content=content,
        media_type="audio/wav",
        headers={"Content-Disposition": f"attachment; filename={uuid4().hex}.wav"}
    )
