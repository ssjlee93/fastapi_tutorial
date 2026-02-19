from fastapi import Depends, FastAPI
from app.enums.enums import ModelName
from app.db.db import create_db_and_tables
from app.config.config import Settings
from functools import lru_cache
from typing import Annotated


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
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Sexy World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# order first checks for this path,
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


# then checks for this path
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# path convertor for path params containing paths
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


def main():
    print("Hello from fastapi-tutorial!")


if __name__ == "__main__":
    main()
