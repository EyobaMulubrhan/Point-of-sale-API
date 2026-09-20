import uuid


class TestSupplierRBAC:

    def test_cashier_cannot_list_suppliers(self, client, cashier_headers, supplier):
        response = client.get("/suppliers/", headers=cashier_headers)
        assert response.status_code == 403

    def test_cashier_cannot_create_supplier(self, client, cashier_headers):
        response = client.post(
            "/suppliers",
            json={"supplier_name": "X", "supplier_email": "x@gmail.com"},
            headers=cashier_headers,
        )
        assert response.status_code == 403


class TestSupplierCRUD:

    def test_manager_creates_supplier(self, client, manager_headers):
        response = client.post(
            "/suppliers",
            json={"supplier_name": "Global Foods", "supplier_email": "gf@gmail.com"},
            headers=manager_headers,
        )
        assert response.status_code == 201
        assert response.json()["supplier_name"] == "Global Foods"

    def test_create_supplier_invalid_email_returns_422(self, client, manager_headers):
        response = client.post(
            "/suppliers",
            json={"supplier_name": "Akirachix", "supplier_email": "noemail"},
            headers=manager_headers,
        )
        assert response.status_code == 422

    def test_create_supplier_missing_name_returns_422(self, client, manager_headers):
        response = client.post(
            "/suppliers", json={"supplier_email": "noname@gmail.com"}, headers=manager_headers
        )
        assert response.status_code == 422

    def test_get_nonexistent_supplier_returns_404(self, client, manager_headers):
        response = client.get(f"/suppliers/{uuid.uuid4()}", headers=manager_headers)
        assert response.status_code == 404

    def test_update_supplier(self, client, manager_headers, supplier):
        response = client.put(
            f"/suppliers/{supplier['supplier_id']}",
            json={"phone_number": "+251978654321"},
            headers=manager_headers,
        )
        assert response.status_code == 200
        assert response.json()["phone_number"] == "+251978654321"

    def test_update_nonexistent_supplier_returns_404(self, client, manager_headers):
        response = client.put(
            f"/suppliers/{uuid.uuid4()}", json={"phone_number": "+251978654321"}, headers=manager_headers
        )
        assert response.status_code == 404

    def test_delete_supplier_without_products_succeeds(self, client, manager_headers, supplier):
        response = client.delete(f"/suppliers/{supplier['supplier_id']}", headers=manager_headers)
        assert response.status_code == 204

    def test_delete_nonexistent_supplier_returns_404(self, client, manager_headers):
        response = client.delete(f"/suppliers/{uuid.uuid4()}", headers=manager_headers)
        assert response.status_code == 404
