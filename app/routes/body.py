from fastapi import APIRouter
from app.internal.models.items import Item

router = APIRouter(
    prefix="/body",
    tags=["body"],
    responses={404: {"description": "Not found"}},
)


# 4. Request Body
@router.post("/items/rb")
async def create_item(item: Item):
    return item


## use a model
@router.post("/items/uam")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


## request body and path parameters
@router.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}


## request body + path parameters + query parameters
@router.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result