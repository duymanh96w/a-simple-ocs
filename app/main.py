from fastapi import FastAPI

from app.config import settings
from app.api.v1 import mobile

from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from redis import Redis


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    app.db_client = AsyncIOMotorClient(settings.db_uri, maxPoolSize=100)
    app.db = app.db_client[settings.db_name]

    x = await app.db.test.find_one()
    print(x)

    app.rdb = Redis(host=settings.redis_host, port=settings.redis_port, db=0)

    return


@app.on_event("shutdown")
async def shutdown_event():
    app.db_client.close()
    app.rdb.close()
    return

app.include_router(mobile.router, prefix='/api/v1/mobile', tags=['mobile'])


@app.get('/api/health-check')
async def heal_check():
    return {'msg': 'hello'}