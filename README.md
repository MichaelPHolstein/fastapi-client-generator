# FastAPI Client Generator

![CI](https://github.com/MichaelPHolstein/fastapi-client-generator/actions/workflows/ci.yml/badge.svg)
![Coverage](https://github.com/MichaelPHolstein/fastapi-client-generator/blob/main/.github/badges/coverage.svg)

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

> ℹ️ **Note:** The examples below use `ClientAlpha`.  
> Once this package reaches a stable version, `Client` will become the default class name.  
> Using `ClientAlpha` avoids breaking existing generated clients in the future.

### 1. Generate a Client from a FastAPI Instance

You can generate a client directly from an in-memory FastAPI application instance.  
This is especially useful during development or when your API is defined within Python rather than deployed yet.

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

### 2. Generate a Client from a Remote OpenAPI URL

You can also generate a client directly from a remote OpenAPI specification URL.  
This is useful when the API documentation is hosted externally or when you want to generate a client without having direct access to the FastAPI application.

In the example below, we generate a client using the public API documentation of a major Dutch retailer, which provides a large and detailed OpenAPI definition:

```python
from fastapi_client_generator import FastapiClientGenerator

api_spec_url="https://api.bol.com/retailer/public/apispec/Retailer%20API%20-%20v10"
FastapiClientGenerator(client_name="bol.com").from_url(api_spec_url)
```

Once generated, you can import and use the client just like any other Python module:

```py
from bol_com import ClientAlpha


dummy_token = "top-secret"
client = ClientAlpha(
    base_url="https://api.bol.com",
    default_headers={"Authorization": f"Bearer {dummy_token}"}
)

ean_rating = client.retailer_products_ean_ratings.get(ean="1234567")

rating = ean_rating.ratings[0].rating
```

### 3. Generate a Client from an OpenAPI File

You can also generate a client directly from a local OpenAPI document.  
This is useful when your API specification is exported as a file (for example, during a CI pipeline, or when the specification is versioned in your project).

The file may be in JSON or YAML format, as long as it contains a valid OpenAPI specification.

```python
from fastapi_client_generator import FastapiClientGenerator

file_path = "./openapi.json"

FastapiClientGenerator(client_name="demo_client").from_file_path(file_path)

```

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

## Generate via CLI

You can also generate clients using the built-in command-line interface (CLI).  
This is convenient for automation, CI pipelines, or working directly with OpenAPI specs without writing Python code.

Two CLI commands are available:

- `from-url` — generate a client from a remote OpenAPI URL
- `from-file` — generate a client from a local OpenAPI file

Both commands use the same parameters shown in the Python examples above.

### 1. Generate a Client from a Remote OpenAPI URL

This CLI example matches the Python example where the API specification is loaded from the public documentation of a Dutch retailer:

```sh
fastapi-client-generator from-url \
  --client-name bol.com \
  --url "https://api.bol.com/retailer/public/apispec/Retailer%20API%20-%20v10"
```

This creates a folder named `bol_com/` containing the generated client.
For how to use that client, see the Python example above in “Generate a Client from a Remote OpenAPI URL”.

### 2. Generate a Client from a Local OpenAPI File

This CLI example matches the earlier Python snippet that loads from a local `openapi.json` file:

```sh
fastapi-client-generator from-file \
  --client-name demo_client \
  --file-path ./openapi.json
```

This creates a folder named `demo_client/` containing the generated client.
For how to use that client, see the Python example above in “Generate a Client from an OpenAPI File”.

## Exception Handling

The generated client raises a custom exception type, `HttpExceptionError`, whenever the server returns a non-2xx HTTP response.  
This ensures that failed API calls are easy to detect, debug, and handle in your application.

### When errors occur

Any endpoint method (e.g. `client.orders.get(...)`, `client.retailer_products.post(...)`) will:

- Return the `requests.Response` object on success
- Raise `HttpExceptionError` on HTTP errors such as:
  - `400 Bad Request`
  - `401 Unauthorized`
  - `403 Forbidden`
  - `404 Not Found`
  - `500 Internal Server Error`
  - …or any other non-successful status code

### Inspecting API errors

The `HttpExceptionError` contains:

- `status_code` — the HTTP status code returned by the API
- `detail` — the raw response body (text), useful for debugging API-side issues

### Example: Handling API errors

```python
from bol_com import ClientAlpha, HttpExceptionError

client = ClientAlpha(
    base_url="https://api.bol.com",
    default_headers={"Authorization": "Bearer YOUR_TOKEN"},
)

try:
    client.retailer_invoices.get(period_end_date="2020-10-24")

except HttpExceptionError as error:
    print(error.status_code)  # e.g. 401
    print(error.detail)       # e.g. {"error":"Unauthorized"}
```

## Contributing

Contributions are welcome!  
If you'd like to improve the generator, fix a bug, enhance the CLI, or add support for additional OpenAPI features, you're more than welcome to contribute.

This project also includes an **advanced class diagram** located at: `mermaid/class-diagram.mmd`.

I encourage contributors to review this diagram before making larger architectural changes.  
It provides a high-level overview of how the main components interact and can greatly help in understanding the internal structure of the generator.

### How to contribute

1. **Fork** the repository
2. Create a new branch for your feature or fix
3. Commit your changes with clear messages
4. Submit a **Pull Request** describing your update

Before submitting a PR, please:

- Ensure the project builds without errors
- Run linting and formatting (Ruff will handle most of it automatically)
- Add tests when introducing new functionality
- Consult the class diagram when modifying or adding core components

If you have ideas, questions, or want to propose new features, feel free to open an **Issue**.  
I appreciate every contribution that helps make this project better.

## License

This project is licensed under the **MIT License**.

You’re free to use, modify, distribute, and integrate this package in both open-source and commercial applications, as long as the terms of the MIT License are followed.

You can find the full license text in the `LICENSE` file included in this repository.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/michaelpholstein)
