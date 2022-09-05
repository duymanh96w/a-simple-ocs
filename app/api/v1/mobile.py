from fastapi import APIRouter, Path, Request, HTTPException, BackgroundTasks

from app.schema.call_detail_record import CallDetailRecord, CDRIn
from app.schema.billing_info import BillingInfo
from app.crud import mobile
from app import redis_op
from app.background_task.mobile import cdr_created
from app.config import settings

import json

router = APIRouter()


@router.get('/{username}/billing', response_model=BillingInfo)
async def api_get_billing_info(
    req: Request,
    username: str = Path(..., min_length=1, max_length=31)
):
    key = 'billing_info_' + username

    # check if data is cached
    cached_billing_info = redis_op.get(key, req.app.rdb)
    if cached_billing_info is not None:
        return json.loads(cached_billing_info)

    # get data from db
    billing_info = await mobile.get_billing_info(username, req.app.db)

    if billing_info is None:
        raise HTTPException(404, detail='Billing info for user %s not found' % username)

    # add to redis for caching
    billing_info.pop('_id', None)
    redis_op.setex(key, settings.redis_cache_ttl, json.dumps(billing_info), req.app.rdb)

    return billing_info


@router.post('/{username}/call', response_model=CallDetailRecord)
async def api_add_cdr(
    req: Request,
    bgr_task: BackgroundTasks,
    cdr_in: CDRIn,
    username: str = Path(..., min_length=1, max_length=31)
):
    call_duration = cdr_in.call_duration
    cdr = CallDetailRecord(username=username, call_duration=call_duration)

    new_cdr = await mobile.add_cdr(cdr, req.app.db)

    bgr_task.add_task(cdr_created, CallDetailRecord(**new_cdr), req.app.db)
    
    return new_cdr