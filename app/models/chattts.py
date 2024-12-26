from typing import Optional, List

from pydantic import BaseModel


class BaseSpeaker(BaseModel):
    name: str


class Text(BaseModel):
    text: str
    speaker: Optional[str] = None


class SpeakerCreate(BaseSpeaker):
    pass


class Speaker(BaseSpeaker):
    id: int
    filepath: str


class SpeakerPublic(Speaker):
    pass


class SpeakersPublic(BaseModel):
    data: List[SpeakerPublic]
    count: int
