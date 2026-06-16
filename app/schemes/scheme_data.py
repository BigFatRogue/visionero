from pydantic import BaseModel
from datetime import datetime


class SourceDataSheme(BaseModel):
    sensor_id: str
    timestamp: datetime
    value: float


class ProcesedDataSheme(SourceDataSheme):
    moving_average: float
    received_at: datetime
    processed_at: datetime
    processing_latency_ms: float


class StatisticDataScheme(BaseModel):
    count_message: int
    procesed_message: int
    invalid_message: int
    avg_processing_latency_ms: float
    count_write_message: int
    count_file_wait_wtrie: int
    count_send_message: int
    count_connection_frontend: int
    count_message_wait_send: int


class HealthCheckSystemSheme(BaseModel):
    full_filepath_data: str 
    python_version: str
    system: str
    pid_process: int