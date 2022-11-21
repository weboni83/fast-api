from datetime import datetime

from fastapi import Depends, Header, HTTPException, Query, status
from typing import Optional, Union
from jose import JWTError, jwt
from pymysql import Timestamp

from . import schemas
from .database import SessionLocal

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .core.config import settings

# bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_token_header(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")


async def get_jwt_token_header(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    expired_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The token has expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
        
        print(f"chek token => {token_data}")

    except jwt.ExpiredSignatureError:
        raise expired_exception
    except JWTError:
        print("jwterror")
        raise credentials_exception

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Depends common parameters
class CommonQueryParams:
    def __init__(self, skip: int = 0, limit: int = 100,q: Union[str, None] = None):
        self.q = q
        self.skip = skip
        self.limit = limit

    