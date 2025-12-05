# FastAPI Client Generator

A tool that automatically generates a **pure Python** API client from an **OpenAPI specification**, designed for seamless integration with **FastAPI** projects.

This package **uses [Ruff](https://github.com/astral-sh/ruff)** to ensure code quality — it automatically **lints and formats** the generated client code, helping maintain a clean and consistent style.

⚠ **NOTE:** This project is still in a early development and may contain bugs

---

## Features

- Generates Python API clients directly from OpenAPI specs
- Designed for compatibility with FastAPI projects
- Pure Python — no external code generation dependencies
- Enforces consistent code style with Ruff (linting + auto-fixing)
- **Generates Pydantic schemas** for both request and response models, including full field validation
- Modular structure for easy extension

## How to use

### From FastAPI-instance

This function will create a FastAPI client based on a FastAPI class instance.

So for example if you create a FastAPI app l, you can provide this class to the client generator.

```py
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

```

A client is now created and can be imported from the new generated folder.

```py
from demo_client import ClientAlpha


client = ClientAlpha(
    base_url="http://localhost:4232",
    default_headers={}
)

root = client.root.get()

item = client.items_item_id.get(
    item_id=1
)


```
