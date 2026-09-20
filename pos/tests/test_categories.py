import uuid


class TestCategoryRBAC:

    def test_cashier_can_list_categories(self, client, cashier_headers, category):
        response = client.get("/categories/", headers=cashier_headers)
        assert response.status_code == 200

    def test_cashier_can_get_single_category(self, client, cashier_headers, category):
        response = client.get(f"/categories/{category['category_id']}", headers=cashier_headers)
        assert response.status_code == 200

    def test_cashier_cannot_create_category(self, client, cashier_headers):
        response = client.post(
            "/categories", json={"category_name": "Snacks"}, headers=cashier_headers
        )
        assert response.status_code == 403

    def test_cashier_cannot_update_category(self, client, cashier_headers, category):
        response = client.put(
            f"/categories/{category['category_id']}",
            json={"category_name": "Updated"},
            headers=cashier_headers,
        )
        assert response.status_code == 403

    def test_cashier_cannot_delete_category(self, client, cashier_headers, category):
        response = client.delete(f"/categories/{category['category_id']}", headers=cashier_headers)
        assert response.status_code == 403

    def test_unauthenticated_request_fails(self, client):
        response = client.get("/categories/")
        assert response.status_code == 401


class TestCategoryCRUD:

    def test_manager_creates_category(self, client, manager_headers):
        response = client.post(
            "/categories",
            json={"category_name": "Snacks", "description": "Chips and crackers"},
            headers=manager_headers,
        )
        assert response.status_code == 201
        assert response.json()["category_name"] == "Snacks"

    def test_create_category_missing_name_returns_422(self, client, manager_headers):
        response = client.post("/categories", json={"description": "no name"}, headers=manager_headers)
        assert response.status_code == 422

    def test_get_nonexistent_category_returns_404(self, client, manager_headers):
        response = client.get(f"/categories/{uuid.uuid4()}", headers=manager_headers)
        assert response.status_code == 404

    def test_update_category(self, client, manager_headers, category):
        response = client.put(
            f"/categories/{category['category_id']}",
            json={"category_name": "Soft Drinks"},
            headers=manager_headers,
        )
        assert response.status_code == 200
        assert response.json()["category_name"] == "Soft Drinks"

    def test_update_nonexistent_category_returns_404(self, client, manager_headers):
        response = client.put(
            f"/categories/{uuid.uuid4()}", json={"category_name": "X"}, headers=manager_headers
        )
        assert response.status_code == 404

    def test_delete_category_without_products_succeeds(self, client, manager_headers, category):
        response = client.delete(f"/categories/{category['category_id']}", headers=manager_headers)
        assert response.status_code == 204

    def test_delete_category_with_products_fails(self, client, manager_headers, category, product):
        response = client.delete(f"/categories/{category['category_id']}", headers=manager_headers)
        assert response.status_code == 400

    def test_delete_nonexistent_category_returns_404(self, client, manager_headers):
        response = client.delete(f"/categories/{uuid.uuid4()}", headers=manager_headers)
        assert response.status_code == 404
