import pytest
import pytest_asyncio
import asyncio
from pathlib import Path
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport

from app.core.config import settings

settings.DATA_FILEPATH = 'test_data/test_data.json'

from app.main import app

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_test_client:
        yield async_test_client

    path = Path(settings.DATA_FILEPATH)
    if path.exists():
        path.unlink()


@pytest.fixture
def correct_message():
    return {
        "sensor_id": "sensor_1",
        "timestamp": "2026-01-15T12:00:00.000Z",
        "value": 12.34
    }


@pytest.fixture
def invalid_message():
    return {
        "sensor_id": "sensort_1",
        "timestamp": "invalid",
        "value": None
    }