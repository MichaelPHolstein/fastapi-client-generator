# FastAPI Client Generator

A utility that automatically generates a **pure-Python API client** from an **OpenAPI specification**, optimized for seamless integration with **FastAPI** applications.

This package uses **[Ruff](https://github.com/astral-sh/ruff)** to ensure consistent code quality — the generated client is automatically **linted and formatted**, producing clean and maintainable Python code.

⚠ **Note:** This project is in early development and may contain bugs. Expect breaking changes until a stable release is published.

## Features

- Generates Python API clients directly from OpenAPI specifications
- Designed specifically for compatibility with FastAPI
- Pure Python — **no external code-generation tools** required
- Ensures consistent style with Ruff (automatic linting + formatting)
- **Generates Pydantic models** for request and response schemas, including full field validation
- Modular project structure for clean organization and easy extension

## Generate within python file

> **Note:** The examples below use `ClientAlpha`.  
> Once this package reaches a stable version, `Client` will become the default class name.  
> Using `ClientAlpha` avoids breaking existing generated clients in the future.

### 1. Generate a Client from a FastAPI Instance

You can generate a client directly from an in-memory FastAPI application instance.  
This is especially useful during development or when your API is defined within Python rather than deployed yet.

#### Example

```python
from typing import Union
from fastapi import FastAPI
from fastapi_client_generator import FastapiClientGenerator

# 1. Create or import a FastAPI application instance
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# 2. Provide the FastAPI app to the client generator
FastapiClientGenerator(client_name="demo_client").from_fastapi(fastapi=app)
```

This will generate a new folder named `demo_client/` containing the auto-generated API client.

Once generated, you can import and use the client just like any other Python module:

```py
from demo_client import ClientAlpha

client = ClientAlpha(
    base_url="http://localhost:4232",
    default_headers={}
)

# Calling the root endpoint
root = client.root.get()

# Calling a parameterized endpoint
item = client.items_item_id.get(
    item_id=1
)
```
