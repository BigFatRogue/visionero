from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates



web_router = APIRouter(tags=['WEB'])

@web_router.get(
        path='/', 
        summary='Начальная страница')
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(name='index.html', request=request)

