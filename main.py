import logging
import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

logger = logging.getLogger(__name__)


TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )


def init_routers(app_):
    from app.controllers import router

    app_.include_router(router)


app = FastAPI()


init_routers(app)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
