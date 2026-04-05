import json
from urllib import response
import pytest
from application.models import db, User, Role
from flask_security.utils import hash_password


# 🔹 Helper to create user with role
# ========================= OWNER LOGIN =========================
def test_owner_login_success(client, create_user):
    create_user("owner1", "1234", "owner")

    response = client.post("/owner-login", json={
        "username": "owner1",
        "password": "1234"
    })
    print(response.status_code)
    print(response.get_json())
    
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data


def test_owner_login_wrong_password(client,create_user):
    create_user( "owner1", "1234", "owner")

    response = client.post("/owner-login", json={
        "username": "owner1",
        "password": "wrong"
    })
   
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "Wrong Password"

def test_owner_login_user_not_found(client):
    response = client.post("/owner-login", json={
        "username": "notexist@test.com",
        "password": "1234"
    })
    print(response.status_code)
    data = response.get_json()
    print(data)

    assert response.status_code == 404


def test_owner_login_wrong_role(client,create_user):
    create_user("user1", "1234", "customer")

    response = client.post("/owner-login", json={
        "username": "user1",
        "password": "1234"
    })

    print(response.status_code)
    data = response.get_json()
    print(data)

    assert response.status_code == 403


# ========================= MANAGER LOGIN =========================
def test_manager_login_success(client,create_user):
    create_user("manager1", "1234", "manager")

    response = client.post("/manager-login", json={
        "username": "manager1",
        "password": "1234"
    })

    print(response.status_code)
    data = response.get_json()
    print(data)


    assert response.status_code == 200


def test_manager_login_wrong_password(client,create_user):
    create_user( "manager1", "1234", "manager")

    response = client.post("/manager-login", json={
        "username": "manager1",
        "password": "wrong"
    })
   
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "Wrong Password"

def test_manager_login_user_not_found(client):
    response = client.post("/manager-login", json={
        "username": "notexist@test.com",
        "password": "1234"
    })
    print(response.status_code)
    data = response.get_json()
    print(data)

    assert response.status_code == 404


def test_manager_login_wrong_role(client,create_user):
    create_user("user1", "1234", "owner")

    response = client.post("/manager-login", json={
        "username": "user1",
        "password": "1234"
    })
    print(response.status_code)
    data = response.get_json()
    print(data)

    assert response.status_code == 403

def test_register_manager_by_owner_success(client, owner_headers):
    # 'owner_headers' should contain the Authentication-Token for an admin/owner
    response = client.post("/register-manager", json={
        "email": "newmanager@salon.com",
        "password": "1234",
        "name": "Branch Manager",
        "dob": "1990-01-01",
        "doj": "2024-04-01",
        "contact": "9888877777",
        "skills": "Operations",
        "branch_name": "Pune Main"
    }, headers=owner_headers) # <--- CRITICAL: Owner must authorize this

    assert response.status_code == 201
    assert response.get_json()["message"] == "Registration successful"
# ========================= STAFF LOGIN =========================
def test_staff_login_success(client,create_user):
    create_user("staff1", "1234", "staff")

    response = client.post("/staff-login", json={
        "username": "staff1",
        "password": "1234"
    })

    print(response.status_code)
    data = response.get_json()
    print(data)

    assert response.status_code == 200


def test_staff_login_wrong_password(client,create_user):
    create_user( "staff1", "1234", "staff")

    response = client.post("/staff-login", json={
        "username": "staff1",
        "password": "wrong"
    })
   
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "Wrong Password"

def test_staff_login_user_not_found(client):
    response = client.post("/staff-login", json={
        "username": "notexist@test.com",
        "password": "1234"
    })
    print(response.status_code)
    data = response.get_json()
    print(data)

    assert response.status_code == 404


def test_staff_login_wrong_role(client,create_user):
    create_user("user1", "1234", "customer")

    response = client.post("/staff-login", json={
        "username": "user1",
        "password": "1234"
    })

    print(response.status_code)
    data = response.get_json()
    print(data)

    assert response.status_code == 403

def test_register_staff_by_manager_success(client, manager_headers):
    # manager_headers should contain the 'Authentication-Token'
    response = client.post("/api/staff", json={
        "email": "newstaff@salon.com",
        "password": "1234",
        "name": "New Stylist",
        "dob": "1995-05-05",
        "doj": "2024-01-01",
        "contact": "9876543210",
        "salary": 50000.0,
        "address": "Pune",
        "skills": "Stylist", 
    }, headers=manager_headers) # <--- CRITICAL: Prove you are a manager

    assert response.status_code == 201
    assert response.get_json()["message"] == "Registration successful"

# ========================= CUSTOMER LOGIN =========================
def test_customer_login_success(client,create_user):
    create_user("cust1", "1234", "customer")

    response = client.post("/customer-login", json={
        "username": "cust1",
        "password": "1234"
    })

    print(response.status_code)
    data = response.get_json()
    print(data)

    assert response.status_code == 200


def test_customer_login_wrong_password(client,create_user):
    create_user( "cust1", "1234", "customer")

    response = client.post("/customer-login", json={
        "username": "cust1",
        "password": "wrong"
    })
   
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "Wrong Password"

def test_customer_login_user_not_found(client):
    response = client.post("/customer-login", json={
        "username": "notexist@test.com",
        "password": "1234"
    })
    print(response.status_code)
    data = response.get_json()
    print(data)

    assert response.status_code == 404


def test_customer_login_wrong_role(client,create_user):
    create_user("user1", "1234", "owner")

    response = client.post("/customer-login", json={
        "username": "user1",
        "password": "1234"
    })

    print(response.status_code)
    data = response.get_json()
    print(data)

    assert response.status_code == 403

# ========================= REGISTER CUSTOMER =========================
def test_register_customer_success(client):
    response = client.post("/register-customer", json={
        "email": "new1",
        "password": "1234",
        "name": "Test User",
        "dob": "2000-01-01",
        "phone": "9999999999",
        "address": "Pune",
        "preferences": ["hair", "spa"]
    })

    print(response.status_code)
    print(response.get_json())

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Registration successful"


def test_register_customer_missing_fields(client):
    response = client.post("/register-customer", json={
        "email": "test1"
    })

    print(response.status_code)
    data = response.get_json()
    print(data)

    assert response.status_code == 400


def test_register_customer_duplicate_email(client):
    # First registration
    client.post("/register-customer", json={
        "email": "dup1",
        "password": "1234",
        "name": "Test",
        "dob": "2000-01-01",
        "phone": "9999999999"})
    # Duplicate
    response = client.post("/register-customer", json={
        "email": "dup1",
        "password": "1234",
        "name": "Test",
        "dob": "2000-01-01",
        "phone": "9999999999"})

    print(response.status_code)
    data = response.get_json()
    print(data)

    assert response.status_code == 400

# ========================= TOKENS =========================
@pytest.mark.no_auth_bypass
def test_token_generation(client,create_user):
    create_user("test_user", "test_pass", "customer")
    res = client.post("/customer-login", json={
        "username": "test_user",
        "password": "test_pass"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "token" in data
    assert data["token"] is not None
    assert isinstance(data["token"], str)

@pytest.mark.no_auth_bypass
def test_no_token(client):
    res = client.get("/api/customer-summary",
    headers={"Accept": "application/json"})
    assert res.status_code in (401, 403)

@pytest.mark.no_auth_bypass
def test_invalid_token(client):
    headers = {"Authentication-Token": "fake_token_123",
    "Accept": "application/json"}

    res = client.get("/api/customer-summary", headers=headers)
    assert res.status_code in (401, 403)

from flask_security.utils import verify_password

def test_password_hashing(client,create_user):
    user = create_user("user1", "1234", "customer")

    assert user.password != "1234"
    assert verify_password("1234", user.password) is True
    assert verify_password("wrong", user.password) is False

@pytest.mark.no_auth_bypass
def test_change_password(client, create_user):
    create_user("user1", "1234", "customer")

    login = client.post(
        "/customer-login",
        json={"username": "user1", "password": "1234"},
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    )

    assert login.status_code == 200
    token = login.get_json()["token"]

    res = client.put(
        "/api/change-password",
        json={
            "current_password": "1234",
            "new_password": "abcd",
            "confirm_password": "abcd"
        },
        headers={
            "Authentication-Token": token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
@pytest.mark.no_auth_bypass
def test_unauthorized_access_wrong_role(client, create_user):
    create_user("cust1", "1234", "customer")

    login = client.post("/customer-login", json={
        "username": "cust1",
        "password": "1234"
    })

    token = login.get_json()["token"]

    res = client.get(
        "/api/staff",
        headers={
            "Authentication-Token": token,
            "Accept": "application/json"
        }
    )

    assert res.status_code == 403