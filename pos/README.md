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

