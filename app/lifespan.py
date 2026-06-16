from app.core.config import settings
from app.core.logging import logger
from pathlib import Path



def create_data_dir() -> None:
    filepath = Path(settings.DATA_FILEPATH)
    parent = filepath.parent
    if not parent.exists():
        try:
            parent.mkdir()
            logger.info(f'Папка [{parent}] успешна создана')
        except Exception:
            logger.error(f'Ошибка создании папки [{parent}]')
        return
    
    logger.info(f'Папка [{parent}] уже существует')
