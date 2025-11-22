from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    id: str
    name: str
    description: Optional[str] = None


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ItemListResponse(BaseModel):
    items: List[Item]
    total: int


fastapi_instance = FastAPI(title="Client Generator Test API", version="1.0.0")


@fastapi_instance.get("/items", response_model=ItemListResponse, summary="List items")
def list_items():
    return ItemListResponse(
        items=[Item(id="item_1", name="Example", description="Demo item")],
        total=1,
    )


@fastapi_instance.post("/items", response_model=Item, summary="Create an item")
def create_item(item: ItemCreate):
    return Item(id="item_2", name=item.name, description=item.description)


@fastapi_instance.get("/items/{item_id}", response_model=Item, summary="Get item by ID")
def get_item(item_id: str):
    return Item(id=item_id, name="Fetched Item", description="Item retrieved by ID")


@fastapi_instance.get(
    "/endpoint/with-description",
    response_model=Item,
    summary="This endpoint includes a description",
    description="This is an endpoint with a description included.",
)
def described_endpoint():
    return Item(id="x", name="described", description="Example")
