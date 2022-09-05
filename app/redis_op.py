from redis import Redis


def get(redis_key: str, rdb: Redis):
    return rdb.get(redis_key)


def setex(redis_key: str, time_to_live: int, value, rdb: Redis):
    return rdb.setex(redis_key, time_to_live, value)
