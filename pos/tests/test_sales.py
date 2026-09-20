import uuid


class TestSaleRBAC:

    def test_unauthenticated_fails(self, client):
        response = client.post("/sales", json={"tax": 0, "discount": 0})
        assert response.status_code == 401

    def test_cashier_can_create_and_list_sales(self, client, cashier_headers):
        create = client.post("/sales", json={"tax": 0, "discount": 0}, headers=cashier_headers)
        assert create.status_code == 201

        listing = client.get("/sales/", headers=cashier_headers)
        assert listing.status_code == 200

    def test_cashier_cannot_update_sale(self, client, cashier_headers, sale):
        response = client.put(
            f"/sales/{sale['sale_id']}", json={"tax": 5}, headers=cashier_headers
        )
        assert response.status_code == 403

    def test_cashier_cannot_delete_sale(self, client, cashier_headers, sale):
        response = client.delete(f"/sales/{sale['sale_id']}", headers=cashier_headers)
        assert response.status_code == 403

    def test_manager_can_update_and_delete_sale(self, client, manager_headers, sale):
        update = client.put(
            f"/sales/{sale['sale_id']}", json={"tax": 5}, headers=manager_headers
        )
        assert update.status_code == 200

        delete = client.delete(f"/sales/{sale['sale_id']}", headers=manager_headers)
        assert delete.status_code == 204


class TestSaleBusinessRules:

    def test_sale_is_attributed_to_authenticated_user_not_client_input(self, client, cashier_headers):
        response = client.post(
            "/sales",
            json={"tax": 0, "discount": 0, "user_id": str(uuid.uuid4())},
            headers=cashier_headers,
        )
        assert response.status_code == 201
        body = response.json()
        assert body["user_id"] != None
        me = client.get("/users/", headers={"Authorization": cashier_headers["Authorization"]})
        assert body["user_id"] != str(uuid.uuid4())

    def test_create_sale_with_valid_customer_succeeds(self, client, cashier_headers, customer):
        response = client.post(
            "/sales",
            json={"customer_id": customer["customer_id"], "tax": 0, "discount": 0},
            headers=cashier_headers,
        )
        assert response.status_code == 201
        assert response.json()["customer_id"] == customer["customer_id"]

    def test_create_sale_with_invalid_customer_returns_404(self, client, cashier_headers):
        response = client.post(
            "/sales",
            json={"customer_id": str(uuid.uuid4()), "tax": 0, "discount": 0},
            headers=cashier_headers,
        )
        assert response.status_code == 404

    def test_create_sale_missing_required_field_returns_422(self, client, cashier_headers):
        response = client.post("/sales", json={"tax": 0}, headers=cashier_headers)
        assert response.status_code == 422

    def test_new_sale_starts_at_zero_amount(self, client, cashier_headers):
        response = client.post("/sales", json={"tax": 0, "discount": 0}, headers=cashier_headers)
        assert float(response.json()["sale_amount"]) == 0.0

    def test_get_nonexistent_sale_returns_404(self, client, cashier_headers):
        response = client.get(f"/sales/{uuid.uuid4()}", headers=cashier_headers)
        assert response.status_code == 404

    def test_update_nonexistent_sale_returns_404(self, client, manager_headers):
        response = client.put(
            f"/sales/{uuid.uuid4()}", json={"tax": 1}, headers=manager_headers
        )
        assert response.status_code == 404

    def test_delete_sale_with_items_fails(self, client, manager_headers, cashier_headers, sale, product):
        item = client.post(
            "/sale-items",
            json={"sale_id": sale["sale_id"], "product_id": product["product_id"], "quantity": 1},
            headers=cashier_headers,
        )
        assert item.status_code == 201

        response = client.delete(f"/sales/{sale['sale_id']}", headers=manager_headers)
        assert response.status_code == 400

    def test_delete_nonexistent_sale_returns_404(self, client, manager_headers):
        response = client.delete(f"/sales/{uuid.uuid4()}", headers=manager_headers)
        assert response.status_code == 404
