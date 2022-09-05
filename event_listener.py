from app.config import settings

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from redis import Redis
from math import ceil
import json
import logging


logging.basicConfig(level=logging.INFO)


db_client = MongoClient(settings.db_uri, maxPoolSize=100)
db = db_client[settings.db_name]

rdb = Redis(host=settings.redis_host, port=settings.redis_port, db=0)


def track_cdr_created(change):
    logging.info(change)
    
    username = change['fullDocument']['username']
    call_duration = change['fullDocument']['call_duration']

    key = 'billing_info_' + username
    cached_info = rdb.get(key)

    if cached_info is not None:
        cached_info = json.loads(cached_info)
        new_info = {
            'username': username,
            'call_count': cached_info['call_count'] + 1,
            'call_block': cached_info['call_block'] + ceil(call_duration/1000/30),
        }

        rdb.setex(key, settings.redis_cache_ttl, value=json.dumps(new_info))


if __name__=="__main__":
    pipeline = [
        {
            '$match': {
                'ns.coll': 'cdr',
                'operationType': {'$in': ['insert']}
            }
        }
    ]


    try:
        resume_token = None
        with db.watch(pipeline) as stream:
            for change in stream:
                track_cdr_created(change)
                resume_token = stream.resume_token
    except PyMongoError:
        if resume_token is None:
            logging.error('There was a failure during ChangeStream initialization...')

        else:
            with db.watch(pipeline, start_after=resume_token) as stream:
                for change in stream:
                    track_cdr_created(change)