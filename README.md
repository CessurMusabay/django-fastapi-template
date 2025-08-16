# Django FastAPI Template

This project is a personal template that combines Django's powerful "batteries-included" tools like the admin panel and ORM with the high performance of FastAPI.

## Prerequisites

- Python 3.9+
- `uv` (install with `pip install uv` or follow instructions on [uv's GitHub](https://github.com/astral-sh/uv))

## Setup

1.  **Create and Activate Virtual Environment**

    ```bash
    uv venv
    source .venv/bin/activate  # On Linux/macOS
    .venv\Scripts\activate     # On Windows
    ```

2.  **Install Dependencies**

    ```bash
    uv pip install -r requirements.txt
    ```

3.  **Run Django Migrations**

    ```bash
    python manage.py migrate
    ```

4.  **Collect Static Files**

    ```bash
    python manage.py collectstatic --noinput
    ```

## Running the Application

To run the FastAPI application, use Uvicorn:

```bash
uvicorn api.main:app --reload
```

This will start the FastAPI server, typically accessible at `http://127.0.0.1:8000` (or a similar address). The `--reload` flag enables auto-reloading on code changes.
