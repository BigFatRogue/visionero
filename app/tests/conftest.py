import pytest
import pytest_asyncio
import asyncio
from pathlib import Path
import shutil
from datetime import datetime, UTC
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.core.config import settings
settings.DATA_FILEPATH = 'test_data/test_data.json'
settings.FLUSH_INTERVAL = 2

from app.core.logging import metrics
metrics.has_test = True


from app.main import create_app


@pytest_asyncio.fixture(scope='function')
async def app():
    yield create_app()

    test_folder_data = Path(settings.DATA_FILEPATH).parent
    if test_folder_data.exists():
        shutil.rmtree(test_folder_data)


@pytest_asyncio.fixture
async def async_client_httpx(app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_test_client:
        yield async_test_client


@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client


@pytest.fixture
def correct_message():
    return {
        "sensor_id": "sensor_1",
        "timestamp": datetime.now(UTC).isoformat(timespec='milliseconds'),
        "value": 12.34
    }


@pytest.fixture
def invalid_message():
    return {
        "sensor_id": "sensort_1",
        "timestamp": "invalid",
        "value": None
    }