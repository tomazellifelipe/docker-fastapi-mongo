from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pymongo import MongoClient
from typing import Optional


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

mongoUrlLocal = 'mongodb://admin:pass@localhost:27017'
mongoUrlDocker = 'mongodb://admin:pass@mongodb:27017' 
mongoDb = 'my-db'
mongoCt = 'my-collection'

client = MongoClient(mongoUrlDocker)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    db = client[mongoDb]
    collection = db[mongoCt]
    new_item = {"item_num": item_id, "name": item.name, "price": item.price}
    created_item = collection.insert_one(new_item)
    return {}

@app.get("/items")
def find_one_item():
    db = client[mongoDb]
    collection = db[mongoCt]
    return collection.find_one(projection={'_id': False})
 
