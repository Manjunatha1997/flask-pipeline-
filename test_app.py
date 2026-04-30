import pytest
from app import app

# -------------------------
# Fixture (test client)
# -------------------------
@pytest.fixture
def client():
    app.testing = True

    with app.test_client() as client:
        yield client


# -------------------------
# LOGIN TESTS
# -------------------------
class TestLoginAPI:

    # ✅ Valid login
    def test_login_success(self, client):
        res = client.post("/login", json={
            "username": "admin",
            "password": "password"
        })

        assert res.status_code == 200
        assert res.is_json
        assert res.get_json()["message"] == "Login successful"


    # ❌ Wrong password
    def test_login_wrong_password(self, client):
        res = client.post("/login", json={
            "username": "admin",
            "password": "wrong"
        })

        assert res.status_code == 401
        assert res.get_json()["message"] == "Invalid credentials"


    # ❌ Wrong username
    def test_login_wrong_username(self, client):
        res = client.post("/login", json={
            "username": "wrong",
            "password": "password"
        })

        assert res.status_code == 401


    # ⚠️ Missing fields (empty body)
    def test_login_missing_body(self, client):
        res = client.post("/login", json={})

        assert res.status_code == 400


    # ⚠️ Missing username only
    def test_login_missing_username(self, client):
        res = client.post("/login", json={
            "password": "password"
        })

        assert res.status_code == 400


    # ⚠️ Missing password only
    def test_login_missing_password(self, client):
        res = client.post("/login", json={
            "username": "admin"
        })

        assert res.status_code == 400


    # ⚠️ Null values
    def test_login_null_values(self, client):
        res = client.post("/login", json={
            "username": None,
            "password": None
        })

        assert res.status_code == 400


    # ⚠️ Wrong data types
    def test_login_wrong_types(self, client):
        res = client.post("/login", json={
            "username": 123,
            "password": True
        })

        assert res.status_code == 400


    # ⚠️ Empty strings
    def test_login_empty_strings(self, client):
        res = client.post("/login", json={
            "username": "",
            "password": ""
        })

        assert res.status_code == 400


    # ❌ GET not allowed
    def test_login_get_method_not_allowed(self, client):
        res = client.get("/login")

        assert res.status_code in [405, 404]


    # ⚠️ No JSON sent
    def test_login_no_json(self, client):
        res = client.post("/login", data="plain text")

        assert res.status_code in [400, 415]