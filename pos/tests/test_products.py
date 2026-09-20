import uuid


class TestProductRBAC:

    def test_cashier_can_list_products(self, client, cashier_headers, product):
        response = client.get("/products", headers=cashier_headers)
        assert response.status_code == 200

    def test_cashier_can_get_single_product(self, client, cashier_headers, product):
        response = client.get(f"/products/{product['product_id']}", headers=cashier_headers)
        assert response.status_code == 200

    def test_cashier_cannot_create_product(self, client, cashier_headers, category):
        response = client.post(
            "/products",
            json={
                "category_id": category["category_id"],
                "product_name": "Sprite",
                "cost_price": 50,
                "selling_price": 90,
                "quantity": 10,
            },
            headers=cashier_headers,
        )
        assert response.status_code == 403

    def test_cashier_cannot_delete_product(self, client, cashier_headers, product):
        response = client.delete(f"/products/{product['product_id']}", headers=cashier_headers)
        assert response.status_code == 403


class TestProductCRUD:

    def test_manager_creates_product(self, client, manager_headers, category):
        response = client.post(
            "/products",
            json={
                "category_id": category["category_id"],
                "product_name": "Fanta",
                "cost_price": 60,
                "selling_price": 110,
                "quantity": 30,
            },
            headers=manager_headers,
        )
        assert response.status_code == 201
        assert response.json()["product_name"] == "Fanta"

    def test_create_product_with_invalid_category_returns_404(self, client, manager_headers):
        response = client.post(
            "/products",
            json={
                "category_id": str(uuid.uuid4()),
                "product_name": "Product",
                "cost_price": 10,
                "selling_price": 20,
                "quantity": 5,
            },
            headers=manager_headers,
        )
        assert response.status_code == 404

    def test_create_product_with_invalid_supplier_returns_404(self, client, manager_headers, category):
        response = client.post(
            "/products",
            json={
                "category_id": category["category_id"],
                "supplier_id": str(uuid.uuid4()),
                "product_name": "Supplier Product",
                "cost_price": 10,
                "selling_price": 20,
                "quantity": 5,
            },
            headers=manager_headers,
        )
        assert response.status_code == 404

    def test_create_product_with_valid_supplier_succeeds(self, client, manager_headers, category, supplier):
        response = client.post(
            "/products",
            json={
                "category_id": category["category_id"],
                "supplier_id": supplier["supplier_id"],
                "product_name": "Supplied Product",
                "cost_price": 10,
                "selling_price": 20,
                "quantity": 5,
            },
            headers=manager_headers,
        )
        assert response.status_code == 201

    def test_create_product_missing_field_returns_422(self, client, manager_headers, category):
        response = client.post(
            "/products",
            json={"category_id": category["category_id"], "product_name": "Incomplete"},
            headers=manager_headers,
        )
        assert response.status_code == 422

    def test_get_nonexistent_product_returns_404(self, client, manager_headers):
        response = client.get(f"/products/{uuid.uuid4()}", headers=manager_headers)
        assert response.status_code == 404

    def test_update_product(self, client, manager_headers, product):
        response = client.put(
            f"/products/{product['product_id']}",
            json={"selling_price": 120},
            headers=manager_headers,
        )
        assert response.status_code == 200
        assert float(response.json()["selling_price"]) == 120.0

    def test_update_product_invalid_category_returns_404(self, client, manager_headers, product):
        response = client.put(
            f"/products/{product['product_id']}",
            json={"category_id": str(uuid.uuid4())},
            headers=manager_headers,
        )
        assert response.status_code == 404

    def test_delete_product_without_sales_succeeds(self, client, manager_headers, product):
        response = client.delete(f"/products/{product['product_id']}", headers=manager_headers)
        assert response.status_code == 204

    def test_delete_product_referenced_in_sale_fails(
        self, client, manager_headers, cashier_headers, product, sale
    ):
        item_response = client.post(
            "/sale-items",
            json={"sale_id": sale["sale_id"], "product_id": product["product_id"], "quantity": 1},
            headers=cashier_headers,
        )
        assert item_response.status_code == 201

        response = client.delete(f"/products/{product['product_id']}", headers=manager_headers)
        assert response.status_code == 400

    def test_delete_nonexistent_product_returns_404(self, client, manager_headers):
        response = client.delete(f"/products/{uuid.uuid4()}", headers=manager_headers)
        assert response.status_code == 404
