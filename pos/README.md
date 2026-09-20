# POS System API

## Description

This project is a Point of Sale (POS) System API built using **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. It provides CRUD operations for managing products, categories, suppliers, customers, users, sales, sale items, payments, and receipts.

## Features

* User Management
* Customer Management
* Product Management
* Category Management
* Supplier Management
* Sales Management
* Payment Management
* Receipt Management

## Technologies Used

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL

## Installation

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Configure the PostgreSQL database in `database.py`.
5. Run the application:

```bash
uvicorn main:app --reload
```

## API Documentation

After starting the server, open:

* Swagger UI: `http://127.0.0.1:8000/docs`

## Running Tests

The test suite uses **pytest** and an isolated **in-memory SQLite** database, it never touches your real PostgreSQL development database. Test isolation is handled automatically by `tests/conftest.py`, which overrides `DATABASE_URL` and `JWT_SECRET` before the app is imported, and gives every test a fresh, empty schema.

1. Install the dependencies (same `requirements.txt` used for the app):

```bash
pip install -r requirements.txt
```

2. Run the full suite from the `pos/` directory:

```bash
pytest
```

Add `-v` for verbose per-test output:

```bash
pytest -v
```

No `.env` file or running PostgreSQL instance is required to run the tests, everything the suite needs is set up automatically.

### Continuous Integration

Every push and pull request automatically runs the full test suite via GitHub Actions (see `.github/workflows/tests.yml`).


