import pytest
from starlette.testclient import TestClient

from app.main import app
from app.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from redis import Redis


@pytest.fixture(scope="module")
def test_app():
    app.db_client = None
    app.db = None

    app.rdb = None
    client = TestClient(app)
    yield client