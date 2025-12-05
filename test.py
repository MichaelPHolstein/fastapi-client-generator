from typing import Union

from fastapi import FastAPI

from fastapi_client_generator import FastapiClientGenerator

# 1. Create or import a FastAPI class instance
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# 2. Provide it to the client generator
FastapiClientGenerator(client_name="demo-client").from_fastapi(fastapi=app)
