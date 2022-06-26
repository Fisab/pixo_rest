from fastapi import FastAPI
from pixo_rest.handlers import health
from pixo_rest.handlers import pixoo


def init_app() -> FastAPI:
    app = FastAPI(
        title='pixoo_rest',
        # root_path=config.root_path,
        root_path_in_servers=False,
        swagger_ui_parameters={'defaultModelsExpandDepth': -1},
    )

    app.include_router(health.router)
    app.include_router(pixoo.router)

    return app


app = init_app()
