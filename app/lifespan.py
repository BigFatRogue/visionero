from app.core.config import settings
from app.core.logging import metrics
from pathlib import Path



def create_data_dir() -> None:
    filepath = Path(settings.DATA_FILEPATH)
    parent = filepath.parent
    if not parent.exists():
        try:
            parent.mkdir()
            metrics.log_info(f'Папка [{parent}] успешна создана')
        except Exception:
            metrics.log_error(f'Ошибка создании папки [{parent}]')
        return
    
    metrics.log_info(f'Папка [{parent}] уже существует')
