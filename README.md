## Схема работы

```
External source
       ↓
  WebSocket /ws/source
       ↓
     Validation (Pydantic)
       ↓
    Preprocessing
       ↓
  Processed message
       ├── → WebSocket /ws/frontend (broadcast)
       └── → local JSONL file (async)

```

## Установка
### Через Poetry (рекомендуется)
``
poetry install
``
### Через pip
``
pip install -r requirements.txt
``

## Настройка окружения
```bash
.env.example    - шаблон настроек
.env            - файл настроек
# Отредактируйте .env при необходимости
```

| Переменная       | Описание                             | По умолчанию           |
| :--------------- | :----------------------------------- | :--------------------- |
| `DATA_FILEPATH`  | Путь к JSONL-файлу для записи        | /data/processed.jsonl |
| `SLIDING_WINDOW` | Размер окна для скользящего среднего | 10                     |
| `FLUSH_INTERVAL` | Интервал сброса буфера на диск (сек) | 1.0                    |
| `FLUSH_COUNT`    | Размер батча для записи в файл       | 100                    |
| `HOST`           | Хост сервера                         | 0.0.0.0                |
| `PORT`           | Порт сервера                         | 8000                   |
| `DEBUG`          | Запуск в режиме отклкди              | True                   |


## Запуск сервера
``>> python run.py``<br>
Сервер будет доступен по адресу: http://localhost:8000

## Запуск генератора тестовых данных
```>> python scripts/source_generator.py --count 10000 --rps 500 --sensors 5 --bad-rate 0.01```

## Подключение фронтенда
Откройте http://localhost:8000 в браузере для визуального мониторинга входящих сообщений. Нажмите клавишу <code>обновить</code>, чтобы увидеть сообщения

## Технологии
- Python 3.11+
- FastAPI
- WebSockets
- Pydantic
- AsyncIO
- aiofiles
- httpx
- pytest

## Схема проекта (endpoints)
| Метод  | Маршрут  | Описание             |
| :----- | :------- | :------------------- |
| `GET`  | `/`      | Страница frontend  |
| `WebSocket` | `ws/source` | Приём и запись данных |
| `WebSocket` | `ws/frontend` | Отправка данных на  frontend |
| `GET` | `system/metrics` | Статистика по полученным данным |
| `GET` | `system/health` | Информация о системе |

## Структура проекта

```
├── app/
│   ├── router/
│   │   ├── router_system.py      # роутеы system
│   ├── core/
│   │   ├── config.py             # Загрузка конфигурации
│   │   ├── file_writer.py        # Асинхронная запись в файл
│   │   ├── process_data.py       # Валидация и модификация входящих данных
│   │   ├── logging.py            # Логирование
│   │   └── templates.py          # Шаблоны для web
│   ├── schemas/
│   │   ├── scheme_data.py        # Pydantic-схемы
│   ├── websocket/
│   │   ├── connection_manager.py # Управление WebSocket-соединениями
│   │   └── ws_router.py          # Вебсокеты
│   ├── main.py
│   └── lifespan.py
├── scripts/
│   └── source_generator.py       # Генератор тестовых данных
├── data/                          # Создаётся автоматически
│   └── data.json
├── .env.example
├── requirements.txt
├── run.py
└── README.md
```

## Тестирование

`>> pytest app/tests/`