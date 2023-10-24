'''Web handler module'''

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    '''Root function'''
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    '''Read item function'''
    return {"item_id": item_id, "q": q}
