from fastapi.encoders import jsonable_encoder

from app.schema.call_detail_record import CallDetailRecord

from motor.motor_asyncio import AsyncIOMotorDatabase
from bson.objectid import ObjectId


async def get_billing_info(username: str, db: AsyncIOMotorDatabase):
    return await db.billing_info.find_one({'username': username})


async def add_cdr(cdr: CallDetailRecord, db: AsyncIOMotorDatabase):
    resp = await db.cdr.insert_one(jsonable_encoder(cdr))
    inserted_id = resp.inserted_id

    new_cdr = await db.cdr.find_one({'_id': ObjectId(inserted_id)})

    return new_cdr
