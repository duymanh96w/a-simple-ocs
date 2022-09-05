from pydantic import BaseModel, Field

from datetime import datetime


class CallDetailRecord(BaseModel):
    username: str
    call_duration: int = Field(..., ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CDRIn(BaseModel):
    call_duration: int = Field(..., ge=0)