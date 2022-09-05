from app.schema.call_detail_record import CallDetailRecord

from motor.motor_asyncio import AsyncIOMotorDatabase
from math import ceil


async def cdr_created(cdr: CallDetailRecord, db: AsyncIOMotorDatabase):
    resp = await db.billing_info.update_one(
        {'username': cdr.username},
        {'$inc': {
            'call_count': 1,
            'call_block': ceil(cdr.call_duration/1000/30)
        }},
        upsert=True
    )

    return resp.modified_count