import pytest
import asyncio
from time import sleep
from httpx import AsyncClient

import json
from pathlib import Path
from fastapi.testclient import TestClient


from app.core.config import settings


@pytest.mark.asyncio
async def test_router_system_metrics(async_client_httpx: AsyncClient):
    response = await async_client_httpx.get(url='/system/metrics')

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_router_system_health(async_client_httpx: AsyncClient):
    response = await async_client_httpx.get(url='/system/health')

    assert response.status_code == 200


def test_ws_source__invalid_message(client: TestClient, invalid_message: dict):
    with client.websocket_connect("ws/source") as source_ws:
        source_ws.send_text(json.dumps(invalid_message))
        sleep(settings.FLUSH_INTERVAL * 2)

        file_path = Path(settings.DATA_FILEPATH)

        assert not file_path.exists()


def test_ws_source__correct_message(client: TestClient, correct_message: dict):
    with client.websocket_connect("/ws/source") as source_ws:
        source_ws.send_text(json.dumps(correct_message))
        sleep(settings.FLUSH_INTERVAL * 2)

        file_path = Path(settings.DATA_FILEPATH)

        assert file_path.parent.exists()

        with open(file_path, 'r') as f:
            lines = f.readlines()
            assert len(lines) >= 1
            
            last_line = json.loads(lines[-1])
            assert last_line["sensor_id"] == correct_message["sensor_id"]
            assert last_line["value"] == correct_message["value"]
            assert last_line["timestamp"] == correct_message["timestamp"].replace('+00:00', '000Z')
            assert "moving_average" in last_line
            assert "received_at" in last_line
            assert "processed_at" in last_line
            assert "processing_latency_ms" in last_line


def test_frontend_receives_messages(client: TestClient, correct_message: dict):
        with client.websocket_connect("/ws/frontend") as frontend_ws:
            with client.websocket_connect("/ws/source") as source_ws:
                source_ws.send_text(json.dumps(correct_message))
                sleep(settings.FLUSH_INTERVAL * 2)
                
                response = frontend_ws.receive_text()
                    
                data = json.loads(response)
                assert data["sensor_id"] == correct_message["sensor_id"]
                assert data["value"] == correct_message["value"]
                assert "moving_average" in data
                    
