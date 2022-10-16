from typing import Union
from fastapi import Body, Depends, FastAPI, HTTPException, Request, Response, status
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .core.config import settings
from .core import helper

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
# CORS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Depends common parameters
class CommonQueryParams:
    def __init__(self, q: Union[str, None] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


# Route
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


@app.get("/users/me", tags=["users"])
async def read_user_me():
    return {"user_id": "the current user"}



@app.post("/users/", response_model=schemas.User, tags=["users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User], tags=["users"])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, tags=["users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#status_code 설정
@app.post("/users/{user_id}/items/", response_model=schemas.Item
, status_code=status.HTTP_201_CREATED
, summary="Create an item"
, response_description="The created item"
, tags=["items"])
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

@app.get("/items/{item_id}", tags=["items"])
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



# @app.get("/items/", response_model=list[schemas.Item], tags=["items"])
# async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
# common parameters 사용하기
@app.get("/items/", response_model=list[schemas.Item], tags=["items"])
async def read_items(commons: CommonQueryParams = Depends()
, db: Session = Depends(get_db)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = crud.get_items(db, skip=commons.skip, limit=commons.limit)
    response.update({"items": items})
    return items

#out schemas 지정하기
@app.put("/items/{item_id}", response_model=schemas.ItemOut, tags=["items"])
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

# 파일업로드
@app.post("/files/")
async def create_files(
    files: list[bytes] = File(description="Multiple files as bytes"),
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(
    files: list[UploadFile] = File(description="Multiple files as UploadFile"),
):
    return {"filenames": [file.filename for file in files]}