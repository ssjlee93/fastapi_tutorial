from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from app.db.db import create_db_and_tables
from app.config.config import Settings
from functools import lru_cache
from typing import Annotated

from app.internal.enums.enums import ModelName
from app.internal.models.items import Item
from app.routes.path import router

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
app.include_router(router)
# 1. first steps
@app.get("/")
async def root():
    return {"message": "Sexy World"}


## order first checks for this path,
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


## then checks for this path
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


## path convertor for path params containing paths
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# 3. Query Parameters
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

## no specification in URI = query parameter
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


## optional parameters
## q: str | None = None means q can be str or None and defaults to None
@app.get("/items/{item_id}/op")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


## type conversion
## especially boolean : True == 1 == true == on == yes
## False == 0 == false == off == no
@app.get("/items/{item_id}/tc")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


## multiple parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


## required parameters
@app.get("/items/{item_id}/rp")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


## mixed
@app.get("/items/{item_id}/mixed")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


# 4. Request Body
@app.post("/items/rb")
async def create_item(item: Item):
    return item


## use a model
@app.post("/items/uam")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


## request body and path parameters
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}


## request body + path parameters + query parameters
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


def main():
    print("Hello from fastapi-tutorial!")


if __name__ == "__main__":
    main()
