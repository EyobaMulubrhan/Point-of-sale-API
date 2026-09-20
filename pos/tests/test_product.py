from fastapi.testclient import TestClient
from pos.main import app

client = TestClient(app)

def test_list_product(client,auth_headers):
    response = client.get("/products", headers=auth_headers)
    print(response.json())
    assert response.status_code == 200

def test_create_product(client,auth_headers):
    category_data = {
        "category_name": "Beverages"
    }
    category_response = client.post("/categories", json=category_data)
    assert category_response.status_code == 201 
    created_category = category_response.json()
    valid_category_id = created_category["category_id"]

    product_data = {
        "product_name": "Coca cola",
        "selling_price": 103.00,
        "cost_price": 80.00,
        "quantity": 50,
        "category_id": valid_category_id 
    }

    response = client.post("/products", json=product_data, headers=auth_headers)
    assert response.status_code == 201



