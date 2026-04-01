import json
from urllib import response
import pytest
from application.models import db, User, Role
from flask_security.utils import hash_password
from conftest import create_user 


# 🔹 Helper to create user with role
# ========================= OWNER LOGIN =========================
def test_owner_login_success(client):
    create_user(client, "owner@test.com", "1234", "owner")

    response = client.post("/owner-login", json={
        "username": "owner@test.com",
        "password": "1234"
    })
    print(response.status_code)
    print(response.get_json())
    
    assert response.status_code == 200
    assert "token" in response.json


def test_owner_login_wrong_password(client):
    create_user(client, "owner@test.com", "1234", "owner")

    response = client.post("/owner-login", json={
        "username": "owner@test.com",
        "password": "wrong"
    })
   
    assert response.status_code == 400
    assert response.json["message"] == "Wrong Password"


def test_owner_login_user_not_found(client):
    response = client.post("/owner-login", json={
        "username": "notexist@test.com",
        "password": "1234"
    })
    print(response.status_code)
    print(response.json)

    assert response.status_code == 404


def test_owner_login_wrong_role(client):
    create_user(client,"user@test.com", "1234", "customer")

    response = client.post("/owner-login", json={
        "username": "user@test.com",
        "password": "1234"
    })

    print(response.status_code)
    print(response.json)

    assert response.status_code == 403


# ========================= MANAGER LOGIN =========================
def test_manager_login_success(client):
    create_user(client,"manager@test.com", "1234", "manager")

    response = client.post("/manager-login", json={
        "username": "manager@test.com",
        "password": "1234"
    })

    print(response.status_code)
    print(response.json)


    assert response.status_code == 200


def test_manager_login_wrong_role(client):
    create_user(client, "user@test.com", "1234", "customer")

    response = client.post("/manager-login", json={
        "username": "user@test.com",
        "password": "1234"
    })
    print(response.status_code)
    print(response.json)

    assert response.status_code == 403


# ========================= STAFF LOGIN =========================
def test_staff_login_success(client):
    create_user(client,"staff@test.com", "1234", "staff")

    response = client.post("/staff-login", json={
        "username": "staff@test.com",
        "password": "1234"
    })

    print(response.status_code)
    print(response.json)

    assert response.status_code == 200


# ========================= CUSTOMER LOGIN =========================
def test_customer_login_success(client):
    create_user(client, "cust@test.com", "1234", "customer")

    response = client.post("/customer-login", json={
        "username": "cust@test.com",
        "password": "1234"
    })

    print(response.status_code)
    print(response.json)

    assert response.status_code == 200


# ========================= REGISTER CUSTOMER =========================
def test_register_customer_success(client):
    response = client.post("/register-customer", json={
        "email": "new@test.com",
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
    assert response.json["message"] == "Registration successful"


def test_register_customer_missing_fields(client):
    response = client.post("/register-customer", json={
        "email": "test@test.com"
    })

    print(response.status_code)
    print(response.json)

    assert response.status_code == 400


def test_register_customer_invalid_dob(client):
    response = client.post("/register-customer", json={
        "email": "test@test.com",
        "password": "1234",
        "name": "Test",
        "dob": "wrong-date",
        "phone": "9999999999"
    })

    print(response.status_code)
    print(response.json)
    
    assert response.status_code == 400


def test_register_customer_duplicate_email(client):
    # First registration
    client.post("/register-customer", json={
        "email": "dup@test.com",
        "password": "1234",
        "name": "Test",
        "dob": "2000-01-01",
        "phone": "9999999999"
    })

    # Duplicate
    response = client.post("/register-customer", json={
        "email": "dup@test.com",
        "password": "1234",
        "name": "Test",
        "dob": "2000-01-01",
        "phone": "9999999999"
    })

    print(response.status_code)
    print(response.json)

    assert response.status_code == 400