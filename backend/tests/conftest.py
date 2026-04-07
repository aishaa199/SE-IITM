"""
conftest.py – shared pytest fixtures for Glow Suite backend tests.

Uses an in-memory SQLite database so tests never touch the real DB.
"""
import pytest
import sys
import os
from datetime import date,datetime

# Make sure Python can find the backend package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import create_app
from application.models import db as _db, Role, User, Staff, Customer, Service, \
    Appointment, Product, Manager
from application.sec import datastore
from flask_security import hash_password


# ─────────────────────────────────────────────────────────────────────────────
# App & DB fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope='session')
def app():
    """Create a test Flask application with an isolated in-memory database."""
    test_app = create_app()
    test_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECURITY_PASSWORD_SALT': 'test-salt',
        'SECRET_KEY': 'test-secret',
        # Disable external AI calls in tests
        # Change this line in your app fixture:
        'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY', 'test-key'),
    })
    with test_app.app_context():
        _db.drop_all()
        _db.create_all()
        _seed_test_data(test_app)
    yield test_app


@pytest.fixture(scope='session')
def client(app):
    """Flask test client (session-scoped — shared across all tests)."""
    return app.test_client()


@pytest.fixture(scope='session')
def db(app):
    with app.app_context():
        yield _db


# ─────────────────────────────────────────────────────────────────────────────
# Seed helper – creates minimal roles + users for each role
# ─────────────────────────────────────────────────────────────────────────────

def _seed_test_data(app):
    with app.app_context():
        # Roles
        for role_name in ['owner', 'manager', 'staff', 'customer']:
            if not Role.query.filter_by(name=role_name).first():
                _db.session.add(Role(name=role_name))
        _db.session.commit()

        # Owner user
        _create_user('test_owner', 'owner@test.com', 'Test@1234', 'owner')

        # Manager user + Manager profile
        mgr_user = _create_user('test_manager', 'mgr@test.com', 'Test@1234', 'manager')
        if not Manager.query.get(mgr_user.id):
            _db.session.add(Manager(
                manager_id=mgr_user.id,
                manager_name='Test Manager',
                manager_email='mgr@test.com',
                manager_contact='+91-9000000001',
                manager_skills='Operations',
                manager_role='Manager',
                manager_dob=date(1985, 1, 1),
                manager_doj=date(2023, 1, 1),
                branch_name='Test Branch',
            ))
        _db.session.commit()

        # Staff user + Staff profile
        stf_user = _create_user('test_staff', 'staff@test.com', 'Test@1234', 'staff')
        if not Staff.query.get(stf_user.id):
            _db.session.add(Staff(
                staff_id=stf_user.id,
                staff_name='Test Stylist',
                staff_contact='+91-9000000002',
                staff_email='staff@test.com',
                staff_skills='Haircut, Facial',
                staff_role='Stylist',
                staff_dob=date(1995, 6, 15),
                staff_doj=date(2023, 3, 1),
                staff_salary=30000,
            ))
        _db.session.commit()

        # Customer user + Customer profile
        cust_user = _create_user('test_customer', 'cust@test.com', 'Test@1234', 'customer')
        if not Customer.query.get(cust_user.id):
            _db.session.add(Customer(
                customer_id=cust_user.id,
                customer_name='Test Customer',
                customer_contact='+91-9000000003',
                customer_dob=date(1998, 8, 20),
                customer_email='cust@test.com',
                customer_address='12 Test Street, Bengaluru',
                number_of_visits=3,
                customer_type='Regular',
                customer_preferences='Haircut',
                customer_available_rewards=100,
                total_spend=4500.0,
            ))
        _db.session.commit()

        # One active service
        if not Service.query.first():
            _db.session.add(Service(
                service_desc='Ladies Haircut & Styling',
                service_category='Hair',
                service_price=550.0,
                service_duration=60,
                service_products='Wella Shampoo',
                service_rating=4.7,
                no_of_reviews=128,
            ))
        _db.session.commit()

        # One product
        if not Product.query.first():
            _db.session.add(Product(
                product_desc='Wella Shampoo 1L',
                product_category_name='Hair',
                product_price=850.0,
                product_min_qoh=5,
                product_curr_qoh=20,
                product_supplier_name='Wella India',
                product_supplier_contact='+91-2266130000',
                product_supplier_email='orders@wella.in',
            ))
        _db.session.commit()
        cust_user = User.query.filter_by(username='test_customer').first()
        stf_user = User.query.filter_by(username='test_staff').first()
        service = Service.query.first()
        # Add one appointment so the Daily Briefing has data to summarize
        if not Appointment.query.first():
            new_appointment = Appointment(
                customer_id=cust_user.id,
                staff_id=stf_user.id,
                appointment_datetime=datetime.now(), # Combined field
                status=0, # 0 for Booked
                feedback_given=False
            )
            
            # 3. Add the service via the relationship list
            if service:
                new_appointment.services.append(service)
            
            _db.session.add(new_appointment)
            _db.session.commit()

def _create_user(username, email, password, role_name):
    existing = datastore.find_user(username=username)
    if existing:
        return existing
    role = Role.query.filter_by(name=role_name).first()
    user = datastore.create_user(
        username=username,
        password=hash_password(password),
        active=True,
    )
    datastore.add_role_to_user(user, role)
    _db.session.commit()
    return user


# ─────────────────────────────────────────────────────────────────────────────
# Token fixtures – call login and return Bearer token string
# ─────────────────────────────────────────────────────────────────────────────

def _login(client, endpoint, username, password):
    rv = client.post(endpoint,
                     json={'username': username, 'password': password},
                     content_type='application/json')
    assert rv.status_code == 200, f"Login failed: {rv.get_json()}"
    return rv.get_json()['token']


@pytest.fixture(scope='session')
def owner_token(client):
    return _login(client, '/owner-login', 'test_owner', 'Test@1234')


@pytest.fixture(scope='session')
def manager_token(client):
    return _login(client, '/manager-login', 'test_manager', 'Test@1234')


@pytest.fixture(scope='session')
def staff_token(client):
    return _login(client, '/staff-login', 'test_staff', 'Test@1234')


@pytest.fixture(scope='session')
def customer_token(client):
    return _login(client, '/customer-login', 'test_customer', 'Test@1234')


# ─────────────────────────────────────────────────────────────────────────────
# Convenience helpers
# ─────────────────────────────────────────────────────────────────────────────

def auth_headers(token):
    """Return headers dict with both auth header styles Flask-Security accepts."""
    return {
        'Authorization': f'Bearer {token}',
        'Authentication-Token': token,
        'Content-Type': 'application/json',
    }
