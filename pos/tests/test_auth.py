class TestRegister:

    def test_register_success(self, client):
        response = client.post(
            "/auth/register",
            json={
                "full_name": "Alya Cashier",
                "username": "alya",
                "password": "alyapass123",
                "user_email": "alya@gmail.com",
            },
        )
        assert response.status_code == 201
        body = response.json()
        assert body["username"] == "alya"
        assert body["role"] == "cashier"
        assert "password" not in body
        assert "password_hash" not in body

    def test_register_without_optional_email(self, client):
        response = client.post(
            "/auth/register",
            json={"full_name": "Buna", "username": "buna", "password": "bunapass123"},
        )
        assert response.status_code == 201
        assert response.json()["user_email"] is None

    def test_register_duplicate_username_fails(self, client, test_user):
        response = client.post(
            "/auth/register",
            json={
                "full_name": "Duplicate",
                "username": test_user["username"],
                "password": "somepass123",
            },
        )
        assert response.status_code == 400

    def test_register_missing_required_field_returns_422(self, client):
        response = client.post(
            "/auth/register",
            json={"username": "nopassword"},
        )
        assert response.status_code == 422

    def test_register_cannot_escalate_to_manager(self, client):

        response = client.post(
            "/auth/register",
            json={
                "full_name": "wrong",
                "username": "wrong",
                "password": "wrongpass123",
                "role": "manager",
            },
        )
        assert response.status_code == 201
        assert response.json()["role"] == "cashier"


class TestLogin:

    def test_login_success(self, client, test_user):
        response = client.post(
            "/auth/login",
            data={"username": test_user["username"], "password": test_user["password"]},
        )
        assert response.status_code == 200
        body = response.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"

    def test_login_wrong_password_fails(self, client, test_user):
        response = client.post(
            "/auth/login",
            data={"username": test_user["username"], "password": "wrongpassword"},
        )
        assert response.status_code == 401

    def test_login_nonexistent_user_fails(self, client):
        response = client.post(
            "/auth/login",
            data={"username": "doesnotexist", "password": "whatever123"},
        )
        assert response.status_code == 401


class TestTokenAuthorization:

    def test_protected_route_without_token_fails(self, client):
        response = client.get("/users/")
        assert response.status_code == 401

    def test_protected_route_with_garbage_token_fails(self, client):
        response = client.get(
            "/users/", headers={"Authorization": "Bearer not-a-real-token"}
        )
        assert response.status_code == 401

    def test_protected_route_with_valid_token_succeeds(self, client, manager_headers):
        response = client.get("/users/", headers=manager_headers)
        assert response.status_code == 200
