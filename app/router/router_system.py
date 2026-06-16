from fastapi import APIRouter
import platform
import os

from app.core.process_data import process_data
from app.core.file_writer import async_file_writer
from app.core.logging import metrics

from app.websocket.connection_manager import connection_manager

from app.schemas.scheme_data import StatisticDataScheme, HealthCheckSystemSheme

router_servise = APIRouter(prefix='/system', tags=['system'])


@router_servise.get('/metrics')
async def get_metrics() -> StatisticDataScheme:
    statistic = {
        **process_data.get_statistics(),
        **async_file_writer.get_statistics(),
        **connection_manager.get_statistics(),
        **metrics.get_statistics()
    }

    response = StatisticDataScheme.model_validate(statistic)

    return response

@router_servise.get('/health')
async def check_health() -> HealthCheckSystemSheme:
    return HealthCheckSystemSheme(
        full_filepath_data = str(async_file_writer.file_path.absolute()),
        python_version = platform.python_version(),
        system = platform.system(),
        pid_process = os.getpid()

    )