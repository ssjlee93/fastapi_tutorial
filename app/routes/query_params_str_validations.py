from fastapi import APIRouter, Query
from typing import Annotated

router = APIRouter(
    prefix="/query-params-str-validations",
    tags=["query-params-str-validations"],
    responses={404: {"description": "Not found"}},
)

# 5. Query Parameters and String Validations¶
@router.get("/items/")
async def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


## additional validation
@router.get("/items/av")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results