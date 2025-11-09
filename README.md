# FastAPI Client Generator

A tool that automatically generates a **pure Python** API client from an **OpenAPI specification**, designed for seamless integration with **FastAPI** projects.

This package **uses [Ruff](https://github.com/astral-sh/ruff)** to ensure code quality — it automatically **lints and formats** the generated client code, helping maintain a clean and consistent style.

⚠ **NOTE:** This project is still a work in progress (WIP) and not finished yet.

---

## Features

- Generates Python API clients directly from OpenAPI specs
- Designed for compatibility with FastAPI projects
- Pure Python — no external code generation dependencies
- Enforces consistent code style with Ruff (linting + auto-fixing)
- **Generates Pydantic schemas** for both request and response models, including full field validation
- Modular structure for easy extension

---

## Todo

- [ ] Add usage instructions
- [ ] Implement API endpoint → Pydantic schema response mapping
- [ ] Add CLI commands for client generation
- [ ] Set up CI/CD for testing and deployment

---

## Example (coming soon)

```python
from fastapi_client_generator import ClientAlpha

client = ClientAlpha(
    base_url="https://api.example.com",
    default_headers={"Authorization": "Bearer token"}
)

response = client.users.get_user(user_id="123")
print(response)
```
