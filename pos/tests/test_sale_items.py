import uuid


class TestSaleItemRBAC:

    def test_cashier_can_create_sale_item(self, client, cashier_headers, sale, product):
        response = client.post(
            "/sale-items",
            json={"sale_id": sale["sale_id"], "product_id": product["product_id"], "quantity": 2},
            headers=cashier_headers,
        )
        assert response.status_code == 201

    def test_cashier_cannot_update_sale_item(self, client, cashier_headers, sale, product):
        item = client.post(
            "/sale-items",
            json={"sale_id": sale["sale_id"], "product_id": product["product_id"], "quantity": 1},
            headers=cashier_headers,
        ).json()

        response = client.put(
            f"/sale-items/{item['sale_item_id']}", json={"quantity": 2}, headers=cashier_headers
        )
        assert response.status_code == 403

    def test_cashier_cannot_delete_sale_item(self, client, cashier_headers, sale, product):
        item = client.post(
            "/sale-items",
            json={"sale_id": sale["sale_id"], "product_id": product["product_id"], "quantity": 1},
            headers=cashier_headers,
        ).json()

        response = client.delete(f"/sale-items/{item['sale_item_id']}", headers=cashier_headers)
        assert response.status_code == 403


class TestSaleItemBusinessRules:

    def test_price_is_derived_from_product_not_client_input(self, client, cashier_headers, sale, product):
        response = client.post(
            "/sale-items",
            json={
                "sale_id": sale["sale_id"],
                "product_id": product["product_id"],
                "quantity": 2,
                "product_price": 0.01,
            },
            headers=cashier_headers,
        )
        assert response.status_code == 201
        body = response.json()
        assert float(body["product_price"]) == 100.0
        assert float(body["subtotal"]) == 200.0

    def test_creating_sale_item_reduces_product_stock(self, client, manager_headers, cashier_headers, sale, product):
        starting_qty = product["quantity"]
        client.post(
            "/sale-items",
            json={"sale_id": sale["sale_id"], "product_id": product["product_id"], "quantity": 5},
            headers=cashier_headers,
        )
        updated_product = client.get(f"/products/{product['product_id']}", headers=manager_headers).json()
        assert updated_product["quantity"] == starting_qty - 5

    def test_creating_sale_item_increases_sale_amount(self, client, cashier_headers, sale, product):
        client.post(
            "/sale-items",
            json={"sale_id": sale["sale_id"], "product_id": product["product_id"], "quantity": 3},
            headers=cashier_headers,
        )
        updated_sale = client.get(f"/sales/{sale['sale_id']}", headers=cashier_headers).json()
        assert float(updated_sale["sale_amount"]) == 300.0

    def test_insufficient_stock_returns_400(self, client, cashier_headers, sale, product):
        response = client.post(
            "/sale-items",
            json={
                "sale_id": sale["sale_id"],
                "product_id": product["product_id"],
                "quantity": product["quantity"] + 100,
            },
            headers=cashier_headers,
        )
        assert response.status_code == 400

    def test_create_sale_item_invalid_sale_returns_404(self, client, cashier_headers, product):
        response = client.post(
            "/sale-items",
            json={"sale_id": str(uuid.uuid4()), "product_id": product["product_id"], "quantity": 1},
            headers=cashier_headers,
        )
        assert response.status_code == 404

    def test_create_sale_item_invalid_product_returns_404(self, client, cashier_headers, sale):
        response = client.post(
            "/sale-items",
            json={"sale_id": sale["sale_id"], "product_id": str(uuid.uuid4()), "quantity": 1},
            headers=cashier_headers,
        )
        assert response.status_code == 404

    def test_update_quantity_recalculates_subtotal_and_stock(
        self, client, manager_headers, cashier_headers, sale, product
    ):
        item = client.post(
            "/sale-items",
            json={"sale_id": sale["sale_id"], "product_id": product["product_id"], "quantity": 2},
            headers=cashier_headers,
        ).json()

        response = client.put(
            f"/sale-items/{item['sale_item_id']}", json={"quantity": 5}, headers=manager_headers
        )
        assert response.status_code == 200
        body = response.json()
        assert body["quantity"] == 5
        assert float(body["subtotal"]) == 500.0

        updated_product = client.get(f"/products/{product['product_id']}", headers=manager_headers).json()
        assert updated_product["quantity"] == product["quantity"] - 5

    def test_update_sale_item_price_field_is_ignored(self, client, manager_headers, cashier_headers, sale, product):
        item = client.post(
            "/sale-items",
            json={"sale_id": sale["sale_id"], "product_id": product["product_id"], "quantity": 1},
            headers=cashier_headers,
        ).json()

        response = client.put(
            f"/sale-items/{item['sale_item_id']}",
            json={"product_price": 1.00},
            headers=manager_headers,
        )
        assert response.status_code == 200
        assert float(response.json()["product_price"]) == 100.0

    def test_deleting_sale_item_restores_stock_and_sale_amount(
        self, client, manager_headers, cashier_headers, sale, product
    ):
        item = client.post(
            "/sale-items",
            json={"sale_id": sale["sale_id"], "product_id": product["product_id"], "quantity": 4},
            headers=cashier_headers,
        ).json()

        response = client.delete(f"/sale-items/{item['sale_item_id']}", headers=manager_headers)
        assert response.status_code == 204

        updated_product = client.get(f"/products/{product['product_id']}", headers=manager_headers).json()
        assert updated_product["quantity"] == product["quantity"]

        updated_sale = client.get(f"/sales/{sale['sale_id']}", headers=cashier_headers).json()
        assert float(updated_sale["sale_amount"]) == 0.0

    def test_get_nonexistent_sale_item_returns_404(self, client, cashier_headers):
        response = client.get(f"/sale-items/{uuid.uuid4()}", headers=cashier_headers)
        assert response.status_code == 404

    def test_delete_nonexistent_sale_item_returns_404(self, client, manager_headers):
        response = client.delete(f"/sale-items/{uuid.uuid4()}", headers=manager_headers)
        assert response.status_code == 404
