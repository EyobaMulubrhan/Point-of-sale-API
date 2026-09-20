
import uuid


class TestPaymentRBAC:

    def test_cashier_can_create_and_list_payments(self, client, cashier_headers, sale):
        create = client.post(
            "/payments",
            json={"sale_id": sale["sale_id"], "paid_amount": 50.00},
            headers=cashier_headers,
        )
        assert create.status_code == 201

        listing = client.get("/payments/", headers=cashier_headers)
        assert listing.status_code == 200

    def test_cashier_cannot_update_payment(self, client, cashier_headers, sale):
        payment = client.post(
            "/payments", json={"sale_id": sale["sale_id"], "paid_amount": 10}, headers=cashier_headers
        ).json()

        response = client.put(
            f"/payments/{payment['payment_id']}", json={"paid_amount": 20}, headers=cashier_headers
        )
        assert response.status_code == 403

    def test_cashier_cannot_delete_payment(self, client, cashier_headers, sale):
        payment = client.post(
            "/payments", json={"sale_id": sale["sale_id"], "paid_amount": 10}, headers=cashier_headers
        ).json()

        response = client.delete(f"/payments/{payment['payment_id']}", headers=cashier_headers)
        assert response.status_code == 403

    def test_manager_can_update_and_delete_payment(self, client, manager_headers, cashier_headers, sale):
        payment = client.post(
            "/payments", json={"sale_id": sale["sale_id"], "paid_amount": 10}, headers=cashier_headers
        ).json()

        update = client.put(
            f"/payments/{payment['payment_id']}", json={"paid_amount": 25}, headers=manager_headers
        )
        assert update.status_code == 200
        assert float(update.json()["paid_amount"]) == 25.0

        delete = client.delete(f"/payments/{payment['payment_id']}", headers=manager_headers)
        assert delete.status_code == 204


class TestPaymentValidation:

    def test_create_payment_invalid_sale_returns_404(self, client, cashier_headers):
        response = client.post(
            "/payments",
            json={"sale_id": str(uuid.uuid4()), "paid_amount": 10},
            headers=cashier_headers,
        )
        assert response.status_code == 404

    def test_create_payment_missing_amount_returns_422(self, client, cashier_headers, sale):
        response = client.post(
            "/payments", json={"sale_id": sale["sale_id"]}, headers=cashier_headers
        )
        assert response.status_code == 422

    def test_get_nonexistent_payment_returns_404(self, client, cashier_headers):
        response = client.get(f"/payments/{uuid.uuid4()}", headers=cashier_headers)
        assert response.status_code == 404

    def test_delete_nonexistent_payment_returns_404(self, client, manager_headers):
        response = client.delete(f"/payments/{uuid.uuid4()}", headers=manager_headers)
        assert response.status_code == 404
