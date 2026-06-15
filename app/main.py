
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

# from app.api.v1.api import router_api_v1
# from app.web.web_router import router_web
# from app.middleware.logging import LoggingMiddleware
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('START APP')

    yield

    print('STOP APP')

origins = ['*']

app = FastAPI(
    lifespan=lifespan
    # docs_url=None, # Отключает /docs
    # redoc_url=None, # Отключает /redoc
    # openapi_url=None # Отключает /openapi.json
)

app.add_middleware(CORSMiddleware, allow_origins=["*"])
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

# app.include_router(router_web)
# app.include_router(router_api_v1, prefix='/api/v1')
