import uuid


class TestCustomerRBAC:

    def test_unauthenticated_fails(self, client):
        response = client.get("/customers/")
        assert response.status_code == 401

    def test_cashier_can_list_and_create(self, client, cashier_headers):
        create = client.post(
            "/customers",
            json={"first_name": "Sam", "last_name": "Lee", "email": "sam@gmail.com"},
            headers=cashier_headers,
        )
        assert create.status_code == 201

        listing = client.get("/customers/", headers=cashier_headers)
        assert listing.status_code == 200

    def test_cashier_can_update_but_not_delete(self, client, cashier_headers, customer):
        update = client.put(
            f"/customers/{customer['customer_id']}",
            json={"phone_number": "+25123456789"},
            headers=cashier_headers,
        )
        assert update.status_code == 200

        delete = client.delete(f"/customers/{customer['customer_id']}", headers=cashier_headers)
        assert delete.status_code == 403

    def test_manager_can_delete_customer(self, client, manager_headers, customer):
        response = client.delete(f"/customers/{customer['customer_id']}", headers=manager_headers)
        assert response.status_code == 204


class TestCustomerCRUD:

    def test_create_customer_missing_required_field_returns_422(self, client, cashier_headers):
        response = client.post(
            "/customers", json={"first_name": "First"}, headers=cashier_headers
        )
        assert response.status_code == 422

    def test_create_customer_invalid_email_returns_422(self, client, cashier_headers):
        response = client.post(
            "/customers",
            json={"first_name": "Bad", "last_name": "Email", "email": "notemail"},
            headers=cashier_headers,
        )
        assert response.status_code == 422

    def test_get_nonexistent_customer_returns_404(self, client, cashier_headers):
        response = client.get(f"/customers/{uuid.uuid4()}", headers=cashier_headers)
        assert response.status_code == 404

    def test_update_nonexistent_customer_returns_404(self, client, cashier_headers):
        response = client.put(
            f"/customers/{uuid.uuid4()}", json={"first_name": "X"}, headers=cashier_headers
        )
        assert response.status_code == 404

    def test_delete_nonexistent_customer_returns_404(self, client, manager_headers):
        response = client.delete(f"/customers/{uuid.uuid4()}", headers=manager_headers)
        assert response.status_code == 404
