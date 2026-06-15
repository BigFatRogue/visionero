from app.core.config import settings
from pathlib import Path


def create_data_dir() -> None:
    filepath = Path(settings.DATA_FILEPATH)
    parent = Path(__file__).parent / filepath.parent
    if not parent.exists():
        try:
            parent.mkdir()
            print(f'Папка [{parent}] успешна создана')
        except Exception:
            print(f'Ошибка создании папки [{parent}]')
        return
    
    print(f'Папка [{parent}] уже существует')
