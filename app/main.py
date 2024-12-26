from fastapi import FastAPI

import app.globals as globals_
from app.api.main import api_router
from app.core.config import settings
from app.core.db import init_db
from chattts import Chat

app = FastAPI(debug=True)


@app.on_event("startup")
async def startup():
    globals_.chattts = Chat()
    globals_.chattts.load(compile=True)
    init_db()


@app.on_event("shutdown")
async def shutdown():
    del globals_.chattts


app.include_router(api_router, prefix=settings.API_V1_STR)
