from fastapi import APIRouter
from fastapi import Body, Depends, FastAPI, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Union

from .. import crud, models, schemas
from ..core import helper, crypto
from ..routers.auth import get_current_active_user
from ..dependencies import get_jwt_token_header, get_db, CommonQueryParams

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_jwt_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/{item_id}", tags=["items"])
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# @router.get("/", tags=["items"])
# async def read_items(q: Union[str, None] = None
# , db: Session = Depends(get_db)):
#     print(q)
#     items = crud.get_items(db,q=q)    
#     return items

# @app.get("/items/", response_model=list[schemas.Item], tags=["items"])
# async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
# common parameters 사용하기
@router.get("/", response_model=list[schemas.Item], tags=["items"])
async def read_items(commons: CommonQueryParams = Depends()
, db: Session = Depends(get_db)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    print(commons.q)
    print(commons.skip)
    print(commons.limit)

    if commons.q:
        items = crud.get_items(db, skip=commons.skip, limit=commons.skip + commons.limit, q=commons.q)
    else:
        items = crud.get_items(db, skip=commons.skip, limit=commons.skip + commons.limit)
    response.update({"items": items})
    return items

#out schemas 지정하기
@router.put("/{item_id}", response_model=schemas.ItemOut, tags=["items"])
async def update_item(
    item_id: int,
    item: schemas.ItemCreate = Body(
        example={
            "title": "Coffee",
            "description": "A very nice Coffee",
            "price": 4100,
            "tax": 373,
        },
    ),
    db: Session = Depends(get_db)
):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    if item.price is not None :
        item.tax = helper.get_tax(item.price)

    if item.price is None: 
        item.tax = None

    crud.update_item(db, item_id, item)

    # amount 는 price - tax 로 생성 후 반환한다. (실제 저장 X)
    item_out = schemas.ItemOut(**item.dict(), amount = item.price - item.tax)
    
    return item_out
