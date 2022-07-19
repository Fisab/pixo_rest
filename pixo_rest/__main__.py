from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pixo_rest.handlers import health
from pixo_rest.handlers import pixoo
from utils.config import get_config
from pixo_rest.service.exceptions import PixooConnectionError


def init_app() -> FastAPI:
    config = get_config()
    app = FastAPI(
        title='pixoo_rest',
        root_path=config.app.root_path,
        root_path_in_servers=False,
        swagger_ui_parameters={'defaultModelsExpandDepth': -1},
    )

    app.include_router(health.router)
    app.include_router(pixoo.router)

    @app.exception_handler(PixooConnectionError)
    async def unicorn_exception_handler(request: Request, exc: PixooConnectionError):
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content={
                'detail': 'Pixoo connection timeout',
            },
        )

    return app


app = init_app()
