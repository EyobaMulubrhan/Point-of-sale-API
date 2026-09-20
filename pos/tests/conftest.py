import os
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["jwt_secret"] = "test-only-secret"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app
from core.security import hash_password
from core.roles import Role
from models.user import User

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def _register_and_login(client, username, password="testpass123", **extra):
    payload = {
        "full_name": extra.pop("full_name", "Test User"),
        "username": username,
        "password": password,
        **extra,
    }
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 201, f"Registration failed: {r.text}"

    r = client.post("/auth/login", data={"username": username, "password": password})
    assert r.status_code == 200, f"Login failed: {r.text}"
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_user(client):
    username = "cashier_user"
    password = "testpass123"
    r = client.post(
        "/auth/register",
        json={
            "full_name": "Cashier User",
            "username": username,
            "password": password,
            "user_email": "cashier@gmail.com",
        },
    )
    assert r.status_code == 201, f"Registration failed: {r.text}"
    return {"username": username, "password": password, **r.json()}


@pytest.fixture
def auth_headers(client, test_user):
    r = client.post(
        "/auth/login",
        data={"username": test_user["username"], "password": test_user["password"]},
    )
    assert r.status_code == 200, f"Login failed: {r.text}"
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_header(auth_headers):
    return auth_headers


@pytest.fixture
def cashier_headers(client):
    return _register_and_login(client, username="cashier2", full_name="Second Cashier")


@pytest.fixture
def manager_user(db_session):
    manager = User(
        full_name="Store Manager",
        username="manager_user",
        password_hash=hash_password("managerpass123"),
        user_email="manager@gmail.com",
        role=Role.MANAGER.value,
    )
    db_session.add(manager)
    db_session.commit()
    db_session.refresh(manager)
    return manager


@pytest.fixture
def manager_headers(client, manager_user):
    r = client.post(
        "/auth/login",
        data={"username": "manager_user", "password": "managerpass123"},
    )
    assert r.status_code == 200, f"Manager login failed: {r.text}"
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def category(client, manager_headers):
    r = client.post(
        "/categories",
        json={"category_name": "Beverages", "description": "Drinks"},
        headers=manager_headers,
    )
    assert r.status_code == 201, r.text
    return r.json()


@pytest.fixture
def supplier(client, manager_headers):
    r = client.post(
        "/suppliers",
        json={"supplier_name": "Beverage Supplies", "supplier_email": "supplier@gmail.com"},
        headers=manager_headers,
    )
    assert r.status_code == 201, r.text
    return r.json()


@pytest.fixture
def product(client, manager_headers, category):
    r = client.post(
        "/products",
        json={
            "category_id": category["category_id"],
            "product_name": "Coca Cola",
            "cost_price": 80.00,
            "selling_price": 100.00,
            "quantity": 50,
        },
        headers=manager_headers,
    )
    assert r.status_code == 201, r.text
    return r.json()


@pytest.fixture
def customer(client, cashier_headers):
    r = client.post(
        "/customers",
        json={"first_name": "Eyoba", "last_name": "Mulubrhan", "email": "eyoba@gmail.com"},
        headers=cashier_headers,
    )
    assert r.status_code == 201, r.text
    return r.json()


@pytest.fixture
def sale(client, cashier_headers):
    r = client.post(
        "/sales",
        json={"tax": 0, "discount": 0},
        headers=cashier_headers,
    )
    assert r.status_code == 201, r.text
    return r.json()




