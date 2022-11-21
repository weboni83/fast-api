from sqlalchemy.orm import Session

from . import models, schemas

from .core import crypto

#users
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    # encryption(string) => 
    # encode with gensalt => 
    # decode when saving to db
    hashed_password = crypto.encryption(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password.decode('utf-8'))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


#items
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_items(db: Session, skip: int = 0, limit: int = 100, q:str= '%'):
    search = "%{}%".format(q)
    return db.query(models.Item).filter(models.Item.title.like(search)).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    db_item.title = item.title
    db_item.price = item.price
    db_item.tax = item.tax
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

