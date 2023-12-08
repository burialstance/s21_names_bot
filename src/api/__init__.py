from fastapi import FastAPI, APIRouter

from . import v1

from src.config.settings import settings

router = APIRouter()

router.include_router(v1.router, prefix='/v1')


@router.get('/healthcheck')
async def healthcheck():
    return f'{settings.APP_TITLE} v{settings.APP_VERSION}'


def register_api_routes(app: FastAPI):
    app.include_router(router, prefix='/api')
