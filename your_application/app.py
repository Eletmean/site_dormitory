# your_application/app.py
from fastapi import APIRouter, Depends
from .wsgi import Item
from sqlalchemy.orm import Session
from .database import get_db

app = APIRouter()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        return {"item_id": item.id, "name": item.name}
    return {"error": "Item not found"}
