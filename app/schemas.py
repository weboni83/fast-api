from pydantic import BaseModel
# :는 유형, =은 할당

class ItemBase(BaseModel):
    title: str
    description: str | None = None

# 생성할 때 필요
class ItemCreate(ItemBase):
    price: float | None = None
    tax: float | None = None

# response model(out)
class ItemOut(BaseModel):
    title: str
    description: str | None = None
    price: float | None = None
    amount: float | None = None
    tax: float | None = None

# 전체 스키마
class Item(ItemCreate):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True

# access token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None