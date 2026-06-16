
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager
from pathlib import Path

from app.core.logging import metrics

from app.core.file_writer import async_file_writer

from app.lifespan import create_data_dir

from app.websocket.ws_router import ws_router
from app.websocket.connection_manager import connection_manager

from app.core.templates import templates

from app.router.system import router_servise
from app.web.web_router import web_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    metrics.log_info('start application')

    create_data_dir()
    await async_file_writer.start()
    await connection_manager.start()

    yield

    await async_file_writer.stop()
    await connection_manager.stop()

    metrics.log_info('end application')

origins = ['*']

app = FastAPI(
    lifespan=lifespan
    # docs_url=None,
    # redoc_url=None,
    # openapi_url=None
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


app.include_router(web_router)
app.include_router(router_servise)
app.include_router(ws_router)

