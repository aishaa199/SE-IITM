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


def test_manager_login_wrong_role(client,create_user):
    create_user("user1", "1234", "customer")

    response = client.post("/manager-login", json={
        "username": "user1",
        "password": "1234"
    })
    print(response.status_code)
    data = response.get_json()
    print(data)

    assert response.status_code == 403


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