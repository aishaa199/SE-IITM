import pytest
from main import app
from application.models import db, Role

@pytest.fixture(autouse=False)
def bypass_auth(monkeypatch,request):
    if "no_auth_bypass" in request.node.keywords:
        return
    def fake_decorator(*args, **kwargs):
        def wrapper(fn):
            return fn
        return wrapper

    # patch everywhere
    monkeypatch.setattr("application.views.auth_required", fake_decorator, raising=False)
    monkeypatch.setattr("application.views.roles_required", fake_decorator, raising=False)

    monkeypatch.setattr("application.resources.auth_required", fake_decorator, raising=False)
    monkeypatch.setattr("application.resources.roles_required", fake_decorator, raising=False)

    monkeypatch.setattr("flask_security.auth_required", fake_decorator, raising=False)
    monkeypatch.setattr("flask_security.roles_required", fake_decorator, raising=False)
    
@pytest.fixture
def app_fixture():
    app.config["TESTING"] = True
    app.config["SECURITY_REDIRECT_BEHAVIOR"] = "spa"
    app.config["SECURITY_UNAUTHORIZED_VIEW"] = None
    # ADD THESE TWO LINES:
    app.config["WTF_CSRF_ENABLED"] = False 
    app.config["SECURITY_TOKEN_AUTHENTICATION_HEADER"] = "Authentication-Token"
    return app

@pytest.fixture
def client(app_fixture):
    with app_fixture.app_context():
        db.create_all()

        roles = ["owner", "manager", "staff", "customer"]
        for r in roles:
            if not Role.query.filter_by(name=r).first():
                db.session.add(Role(name=r))

        db.session.commit()

        yield app_fixture.test_client()

        db.session.remove()
        db.drop_all()

from application.models import User
from flask_security.utils import hash_password
@pytest.fixture
def headers_for_role(client, create_user):
    def _get_headers(role_name):
        username = f"test{role_name}" 
        password = "password123"
        
        create_user(username, password, role_name)
        
        # Use the role-specific login route you defined: /owner-login, /manager-login, etc.
        login_url = f"/{role_name}-login"
        res = client.post(login_url, json={
            "username": username,
            "password": password
        })
        
        data = res.get_json()

        if res.status_code != 200:
            pytest.fail(f"Login failed for {role_name} at {login_url}. Status: {res.status_code}, Error: {data}")

        # Try to find the token based on your different possible response structures
        token = None
        if "token" in data:
            token = data["token"]
        elif "response" in data and "user" in data["response"]:
            token = data["response"]["user"].get("authentication_token")
            
        if not token:
            pytest.fail(f"Could not find token in response. Data: {data}")
            
        return {
            "Authentication-Token": token,
            "Content-Type": "application/json"
        }
            
    return _get_headers

@pytest.fixture
def manager_headers(headers_for_role):
    return headers_for_role("manager")

@pytest.fixture
def owner_headers(headers_for_role):
    return headers_for_role("owner")

@pytest.fixture
def staff_headers(headers_for_role):
    return headers_for_role("staff")

@pytest.fixture
def customer_headers(headers_for_role):
    return headers_for_role("customer")
@pytest.fixture
def create_user():
    def _create_user(username, password, role_name):
        from application.sec import datastore # Ensure this points to your datastore
        
        # Check if user already exists to avoid duplicate seed errors
        user = datastore.find_user(username=username)
        if not user:
            # Create user via datastore
            user = datastore.create_user(
                username=username,
                password=hash_password(password),
                active=True
            )
            db.session.commit()

        # Check if user already has the role
        role = Role.query.filter_by(name=role_name).first()
        if role not in user.roles:
            datastore.add_role_to_user(user, role)
            db.session.commit()
        
        # Force a refresh to ensure roles are loaded
        db.session.refresh(user)
        return user

    return _create_user

@pytest.fixture
def get_token(client, create_user):
    def _get_token(username, password, role):
        create_user(username, password, role)

        res = client.post(f"/{role}-login", json={
            "username": username,
            "password": password
        })

        return res.get_json()["token"]

    return _get_token

@pytest.fixture
def create_customer( create_user):
    def _create_customer(username, name, email):
        # 1. Create the base User with 'customer' role
        user = create_user(username, "password123", "customer")
        
        # 2. Create the Customer profile linked to that user
        from application.models import Customer
        from datetime import date
        customer = Customer(
            customer_id=user.id, # Link via PK/FK
            customer_name=name,
            customer_contact="1234567890",
            customer_dob=date(1990, 1, 1),
            customer_email=email,
            customer_type="Regular"
        )
        db.session.add(customer)
        db.session.commit()
        return customer
    return _create_customer

@pytest.fixture
def create_staff(create_user):
    def _create_staff(username, password, active=True):
        user = create_user(username, password, "staff")

        user.active = active
        db.session.commit()

        from application.models import Staff
        from datetime import date

        staff = Staff(
            user=user,  # ✅ correct relation
            staff_name=username,
            staff_contact="9999999999",
            staff_email=f"{username}@test.com",
            staff_skills="haircut",
            staff_role="stylist",
            staff_dob=date(2000, 1, 1),
            staff_salary=10000
        )

        db.session.add(staff)
        db.session.commit()

        return staff

    return _create_staff

@pytest.fixture
def create_attendance():
    def _create_attendance(staff_id, dt):
        from application.models import StaffAttendance

        record = StaffAttendance(
            staff_id=staff_id,
            register_datetime=dt
        )

        db.session.add(record)
        db.session.commit()

        return record

    return _create_attendance