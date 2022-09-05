from pydantic import BaseModel, Field


class BillingInfo(BaseModel):
    username: str
    call_count: int
    call_block: int