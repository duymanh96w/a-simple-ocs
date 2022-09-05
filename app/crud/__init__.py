from pydantic import BaseModel, Field


class Billing(BaseModel):
    username: str = Field(..., min_length=1, max_length=31)
    call_count: int = Field(..., gt=0)
    call_block: int = Field(..., ge=0)