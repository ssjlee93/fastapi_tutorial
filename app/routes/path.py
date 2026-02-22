from fastapi import APIRouter


router = APIRouter(
    prefix="/path",
    tags=["path"],
    responses={404: {"description": "Not found"}},
)

# 2. Path Parameters
@router.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
