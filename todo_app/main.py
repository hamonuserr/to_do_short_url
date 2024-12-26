from typing import List, Optional, Union, Annotated
from fastapi import FastAPI, HTTPException, Depends, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session


from database import SessionLocal, engine, Base
from models import TodoItem as TodoItemModel
from authx import AuthX, AuthXConfig

Base.metadata.create_all(bind=engine)

app = FastAPI()

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET KEY"
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

working_config = AuthX(config=config)

class UserLogin(BaseModel):
    username: str
    password: str


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TodoCreateList(BaseModel):
    items_list: List[TodoCreate]


class TodoItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    class Config:
        orm_mode = True


class TodoItemList(BaseModel):
    items: List[TodoItem]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/login")
def login(credentials: Annotated[UserLogin, Depends()], response: Response):
    if credentials.username == "admin" and credentials.password == "admin":
        token = working_config.create_access_token(uid = "1337")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")


@app.get("/items", response_model=List[TodoItem], dependencies = [Depends(working_config.access_token_required)])
def get_items(db: Session = Depends(get_db), title: Union[str, None] = None):
    items = db.query(TodoItemModel).all() if title is None else db.query(TodoItemModel).filter(
        TodoItemModel.title == title)
    return items


@app.get("/items/{item_id}", response_model=TodoItem, dependencies = [Depends(working_config.access_token_required)])
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(TodoItemModel).filter(TodoItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items", response_model=TodoItem, dependencies = [Depends(working_config.access_token_required)])
def create_item(item: TodoCreate, db: Session = Depends(get_db)):
    new_item = TodoItemModel(
        title=item.title,
        description=item.description,
        completed=item.completed
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.put("/items/{item_id}", response_model=TodoItem, dependencies = [Depends(working_config.access_token_required)])
def update_item(item_id: int, item: TodoCreate, db: Session = Depends(get_db)):
    db_item = db.query(TodoItemModel).filter(TodoItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.title = item.title
    db_item.description = item.description
    db_item.completed = item.completed
    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/items/{item_id}", dependencies = [Depends(working_config.access_token_required)])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(TodoItemModel).filter(TodoItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted"}
