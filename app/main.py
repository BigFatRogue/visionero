
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager
from pathlib import Path

from app.core.file_writer import async_file_writer

from app.lifespan import create_data_dir

from app.websocket.ws_router import ws_router
from app.websocket.connection_manager import connection_manager

from app.core.templates import templates


from app.router.system import router_servise
from app.web.web_router import web_router
# from app.middleware.logging import LoggingMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    print('START APP')

    create_data_dir()
    await async_file_writer.start()
    await connection_manager.start()

    yield

    await async_file_writer.stop()
    await connection_manager.stop()

    print('STOP APP')

origins = ['*']

app = FastAPI(
    lifespan=lifespan
    # docs_url=None, # Отключает /docs
    # redoc_url=None, # Отключает /redoc
    # openapi_url=None # Отключает /openapi.json
)

app.mount("/web/static", StaticFiles(directory=Path(__file__).parent / "web/static"), name="static")
app.state.templates = templates

app.add_middleware(
    CORSMiddleware,
     allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(LoggingMiddleware)

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     response = await call_next(request)
#     return response

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     print(exc.errors())
#     return JSONResponse(
#         status_code=422,
#         content={"detail": "Ошибка валидации данных", "errors": exc.errors()},
#     )

app.include_router(web_router)
app.include_router(router_servise)
app.include_router(ws_router)

