from typing import Self
import json
from datetime import datetime, UTC
from collections import deque
from pydantic import ValidationError

from app.core.config import settings

from app.core.logging import metrics

from app.schemas.scheme_data import SourceDataSheme, ProcesedDataSheme


class ProcesData:
    def __init__(self):
        self.source_data: SourceDataSheme | None = None
        self.procesed_data: ProcesedDataSheme | None = None
        self.values_sensor_id: dict[int, deque] = {}
        
        self.count_message = 0
        self.procesed_message = 0
        self.invalid_message = 0
        self.avg_processing_latency_ms = 0.0

    def __call__(self, data: str) -> Self:
        received_at = datetime.now(UTC)
        self.count_message += 1

        try:
            self.source_data = SourceDataSheme.model_validate_json(data)
        except ValidationError as e:
            self.source_data = None
            self.procesed_data = None
            self.invalid_message += 1
            metrics.log_error('validate error', e.errors(), False, False)
            return self

        moving_average = self._calc_averge(self.source_data.sensor_id, self.source_data.value)
        processed_at = datetime.now(UTC)

        update_data = {
            'moving_average': moving_average,
            'received_at': received_at.isoformat(timespec='milliseconds'),
            'processed_at': processed_at.isoformat(timespec='milliseconds'),
            'processing_latency_ms': 0
        }

        proces_data_dict = self.source_data.model_dump()
        proces_data_dict.update(update_data)

        self.procesed_data = ProcesedDataSheme.model_validate(proces_data_dict)
        
        self.procesed_message += 1
        
        processed_at = datetime.now(UTC)
        
        processing_latency_ms = (processed_at - received_at).total_seconds() * 1000
        self.procesed_data.processing_latency_ms = processing_latency_ms
        
        self.avg_processing_latency_ms = (self.avg_processing_latency_ms * (self.count_message - 1) + processing_latency_ms) / self.count_message
        
        return self
    
    def _calc_averge(self, sensor_id: str, value: float) -> float:
        if sensor_id is not None:
            if sensor_id in self.values_sensor_id:
                self.values_sensor_id[sensor_id].append(value)
            else:
                self.values_sensor_id[sensor_id] = deque([value], maxlen=settings.SLIDING_WINDOW)
        return sum(self.values_sensor_id[sensor_id]) / len(self.values_sensor_id[sensor_id])

    def to_json(self) -> str | None:
        if self.procesed_data is not None:
            return self.procesed_data.model_dump_json()
    
    def get_statistics(self) -> dict:
        return {
            'count_message': self.count_message,
            'procesed_message': self.procesed_message,
            'invalid_message': self.invalid_message,
            'avg_processing_latency_ms': self.avg_processing_latency_ms
        }

    def __str__(self) -> str:
        return f'{self.count_message=}, {self.procesed_message=}, {self.invalid_message=}, {self.avg_processing_latency_ms=}'

    def __repr__(self) -> str:
        return self.__str__()

process_data = ProcesData()