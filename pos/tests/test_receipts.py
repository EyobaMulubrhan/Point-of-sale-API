import uuid


class TestReceiptRBAC:

    def test_cashier_can_create_and_list_receipts(self, client, cashier_headers, sale):
        create = client.post(
            "/receipts",
            json={"sale_id": sale["sale_id"], "receipt_number": "RCPT-0001"},
            headers=cashier_headers,
        )
        assert create.status_code == 201

        listing = client.get("/receipts/", headers=cashier_headers)
        assert listing.status_code == 200

    def test_cashier_cannot_update_or_delete_receipt(self, client, cashier_headers, sale):
        receipt = client.post(
            "/receipts",
            json={"sale_id": sale["sale_id"], "receipt_number": "RCPT-0002"},
            headers=cashier_headers,
        ).json()

        update = client.put(
            f"/receipts/{receipt['receipt_id']}",
            json={"receipt_number": "RCPT-9999"},
            headers=cashier_headers,
        )
        assert update.status_code == 403

        delete = client.delete(f"/receipts/{receipt['receipt_id']}", headers=cashier_headers)
        assert delete.status_code == 403

    def test_manager_can_update_and_delete_receipt(self, client, manager_headers, cashier_headers, sale):
        receipt = client.post(
            "/receipts",
            json={"sale_id": sale["sale_id"], "receipt_number": "RCPT-0003"},
            headers=cashier_headers,
        ).json()

        update = client.put(
            f"/receipts/{receipt['receipt_id']}",
            json={"receipt_number": "RCPT-0003-B"},
            headers=manager_headers,
        )
        assert update.status_code == 200

        delete = client.delete(f"/receipts/{receipt['receipt_id']}", headers=manager_headers)
        assert delete.status_code == 204


class TestReceiptValidation:

    def test_create_receipt_invalid_sale_returns_404(self, client, cashier_headers):
        response = client.post(
            "/receipts",
            json={"sale_id": str(uuid.uuid4()), "receipt_number": "RCPT-GHOST"},
            headers=cashier_headers,
        )
        assert response.status_code == 404

    def test_duplicate_receipt_number_returns_400_not_500(self, client, cashier_headers, sale):
        first = client.post(
            "/receipts",
            json={"sale_id": sale["sale_id"], "receipt_number": "RCPT-DUPLICATE"},
            headers=cashier_headers,
        )
        assert first.status_code == 201

        second_sale = client.post("/sales", json={"tax": 0, "discount": 0}, headers=cashier_headers).json()
        second = client.post(
            "/receipts",
            json={"sale_id": second_sale["sale_id"], "receipt_number": "RCPT-DUPLICATE"},
            headers=cashier_headers,
        )
        assert second.status_code == 400

    def test_create_receipt_missing_number_returns_422(self, client, cashier_headers, sale):
        response = client.post(
            "/receipts", json={"sale_id": sale["sale_id"]}, headers=cashier_headers
        )
        assert response.status_code == 422

    def test_get_nonexistent_receipt_returns_404(self, client, cashier_headers):
        response = client.get(f"/receipts/{uuid.uuid4()}", headers=cashier_headers)
        assert response.status_code == 404

    def test_delete_nonexistent_receipt_returns_404(self, client, manager_headers):
        response = client.delete(f"/receipts/{uuid.uuid4()}", headers=manager_headers)
        assert response.status_code == 404
