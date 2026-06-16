from fastapi import Depends
from typing import Annotated

from app.core.logging import Metrics

metrics = None

def get_metrics() -> Metrics:
    global metrics
    if metrics is None:
        metrics = Metrics()
    return metrics

MetricsDep = Annotated[Metrics, Depends(get_metrics)]