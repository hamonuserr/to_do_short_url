import string
import random
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from models import URLItem

Base.metadata.create_all(bind=engine)

app = FastAPI()


class URLCreate(BaseModel):
    url: HttpUrl


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@app.post("/shorten")
def shorten_url(item: URLCreate, db: Session = Depends(get_db)):
    for _ in range(10):
        short_id = generate_short_id()
        print(short_id)
        existing = db.query(URLItem).filter(URLItem.short_id == short_id).first()
        if not existing:
            new_item = URLItem(short_id=short_id, full_url=str(item.url))
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            return {"short_url": f"http://localhost:8000/{short_id}"}
    raise HTTPException(status_code=500, detail="Не удалось сгенерировать короткую ссылку")


@app.get("/{short_id}")
def redirect_to_full(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    return RedirectResponse(url=url_item.full_url, status_code=302)   # изменен статус для редиректа


@app.get("/stats/{short_id}")
def get_stats(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    return {
        "short_id": url_item.short_id,
        "full_url": url_item.full_url
    }


@app.put("/{short_id}")
def update_item(item: URLCreate, short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Url not found")
    url_item.full_url = str(item.url)
    db.commit()
    db.refresh(url_item)
    return url_item


@app.delete("/{short_id}")
def delete_url(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Url not found")
    db.delete(url_item)
    db.commit()
    return {"message": "Url deleted"}
