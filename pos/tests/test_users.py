class TestUserRBAC:

    def test_cashier_cannot_list_users(self, client, cashier_headers):
        response = client.get("/users/", headers=cashier_headers)
        assert response.status_code == 403

    def test_cashier_cannot_create_user(self, client, cashier_headers):
        response = client.post(
            "/users/",
            json={
                "full_name": "New",
                "username": "newuser",
                "password": "newpass123",
                "role": "cashier",
            },
            headers=cashier_headers,
        )
        assert response.status_code == 403

    def test_manager_can_list_users(self, client, manager_headers):
        response = client.get("/users/", headers=manager_headers)
        assert response.status_code == 200


class TestUserCRUD:

    def test_manager_creates_user(self, client, manager_headers):
        response = client.post(
            "/users/",
            json={
                "full_name": "New Cashier",
                "username": "newcashier",
                "password": "newpass123",
                "role": "cashier",
            },
            headers=manager_headers,
        )
        assert response.status_code == 201
        body = response.json()
        assert body["username"] == "newcashier"
        assert "password" not in body
        assert "password_hash" not in body

    def test_created_user_password_is_hashed_not_plaintext(self, client, manager_headers, db_session):
        response = client.post(
            "/users/",
            json={
                "full_name": "Hash Check",
                "username": "hashcheck",
                "password": "plaintextpass123",
                "role": "cashier",
            },
            headers=manager_headers,
        )
        assert response.status_code == 201

        from models.user import User
        stored = db_session.query(User).filter(User.username == "hashcheck").first()
        assert stored.password_hash != "plaintextpass123"


        login = client.post(
            "/auth/login", data={"username": "hashcheck", "password": "plaintextpass123"}
        )
        assert login.status_code == 200

    def test_create_user_duplicate_username_fails(self, client, manager_headers, test_user):
        response = client.post(
            "/users/",
            json={
                "full_name": "Dup",
                "username": test_user["username"],
                "password": "duppass123",
                "role": "cashier",
            },
            headers=manager_headers,
        )
        assert response.status_code == 400

    def test_create_user_invalid_role_returns_422(self, client, manager_headers):
        response = client.post(
            "/users/",
            json={
                "full_name": "NoRole",
                "username": "norole",
                "password": "norolepass123",
                "role": "superadmin",
            },
            headers=manager_headers,
        )
        assert response.status_code == 422

    def test_get_user_by_id(self, client, manager_headers, test_user):
        response = client.get(f"/users/{test_user['user_id']}", headers=manager_headers)
        assert response.status_code == 200
        assert response.json()["username"] == test_user["username"]

    def test_get_nonexistent_user_returns_404(self, client, manager_headers):
        import uuid
        response = client.get(f"/users/{uuid.uuid4()}", headers=manager_headers)
        assert response.status_code == 404

    def test_update_user_password_rehashes_and_old_password_stops_working(
        self, client, manager_headers, test_user
    ):
        response = client.patch(
            f"/users/{test_user['user_id']}",
            json={"password": "newpassword123"},
            headers=manager_headers,
        )
        assert response.status_code == 200

        old_login = client.post(
            "/auth/login",
            data={"username": test_user["username"], "password": test_user["password"]},
        )
        assert old_login.status_code == 401

        new_login = client.post(
            "/auth/login",
            data={"username": test_user["username"], "password": "newpassword123"},
        )
        assert new_login.status_code == 200

    def test_update_user_to_duplicate_username_fails(self, client, manager_headers, test_user):
        other = client.post(
            "/users/",
            json={
                "full_name": "Other",
                "username": "otheruser",
                "password": "otherpass123",
                "role": "cashier",
            },
            headers=manager_headers,
        ).json()

        response = client.patch(
            f"/users/{other['user_id']}",
            json={"username": test_user["username"]},
            headers=manager_headers,
        )
        assert response.status_code == 400

    def test_update_nonexistent_user_returns_404(self, client, manager_headers):
        import uuid
        response = client.patch(
            f"/users/{uuid.uuid4()}", json={"full_name": "X"}, headers=manager_headers
        )
        assert response.status_code == 404

    def test_delete_user(self, client, manager_headers, test_user):
        response = client.delete(f"/users/{test_user['user_id']}", headers=manager_headers)
        assert response.status_code == 204

        get_response = client.get(f"/users/{test_user['user_id']}", headers=manager_headers)
        assert get_response.status_code == 404

    def test_delete_nonexistent_user_returns_404(self, client, manager_headers):
        import uuid
        response = client.delete(f"/users/{uuid.uuid4()}", headers=manager_headers)
        assert response.status_code == 404
