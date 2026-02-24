from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from app.db.db import create_db_and_tables
from app.config.config import Settings
from functools import lru_cache
from typing import Annotated

from app.internal.models.items import Item
from app.routes import path, query, body, query_params_str_validations

app = FastAPI()


# settings related
@lru_cache
def get_settings():
    return Settings()


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "app_name": settings.PROJECT_NAME,
        "database_url": settings.DATABASE_URL,
    }


# db related
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


# router
app.include_router(path.router)
app.include_router(query.router)
app.include_router(body.router)
app.include_router(query_params_str_validations.router)

# 1. first steps
@app.get("/")
async def root():
    return {"message": "Sexy World"}


def main():
    print("Hello from fastapi-tutorial!")


if __name__ == "__main__":
    main()
