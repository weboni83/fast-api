from fastapi import APIRouter
from fastapi import Body, Depends, FastAPI, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .. import crud, models, schemas
from ..core import helper, crypto
from ..routers.auth import get_current_active_user
from ..dependencies import get_jwt_token_header, get_db, CommonQueryParams

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_jwt_token_header)],
    responses={404: {"description": "Not found"}},
)


# @router.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=form_data.username)
#     if not db_user:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     if not crypto.checkpw(form_data.password, db_user.hashed_password) :
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     print(db_user.email)

#     return {"access_token": db_user.email, "token_type": "bearer"}



@router.get("/me", response_model=schemas.User, tags=["users"])
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@router.get("/me/items/")
async def read_users_me_items(current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=current_user.id)
    print(db_user.items)
    return [{"owner": current_user.id, "items": db_user.items}]


@router.post("/", response_model=schemas.User, tags=["users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# @router.get("/", response_model=list[schemas.User], tags=["users"])
# async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users
# common parameters 사용하기
@router.get("/", response_model=list[schemas.User], tags=["users"])
async def read_users(commons: CommonQueryParams = Depends()
, db: Session = Depends(get_db)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    users = crud.get_users(db, skip=commons.skip, limit=commons.limit)
    response.update({"users": users})
    return users


@router.get("/{user_id}", response_model=schemas.User, tags=["users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


#status_code 설정
@router.post("/{user_id}/items/", response_model=schemas.Item
, status_code=status.HTTP_201_CREATED
, summary="Create an item"
, response_description="The created item"
, tags=["users"])
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    if item.price is not None :
        item.tax = helper.get_tax(item.price)

    if item.price is None: 
        item.tax = None

    return crud.create_user_item(db=db, item=item, user_id=user_id)