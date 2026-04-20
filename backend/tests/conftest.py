"""
conftest.py – shared pytest fixtures for Glow Suite backend tests.

Uses an in-memory SQLite database so tests never touch the real DB.
test_config is injected into create_app() BEFORE db.init_app() so the
engine is bound to ':memory:' from the very first DB operation.
"""
import pytest
import sys
import os
from datetime import date

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
    """Flask app backed by an isolated in-memory SQLite DB."""
    test_app = create_app(test_config={
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECURITY_PASSWORD_SALT': 'test-salt',
        'SECRET_KEY': 'test-secret',
        'ANTHROPIC_API_KEY': 'test-key',
        # Disable scheduled jobs during tests
        'SCHEDULER_API_ENABLED': False,
        'JOBS': [],
    })
    with test_app.app_context():
        _db.create_all()
        _seed_test_data(test_app)
    yield test_app


@pytest.fixture(scope='session')
def client(app):
    # use_cookies=False prevents session-cookie leakage between tests
    # (staff POST cookies must not bleed into subsequent manager requests).
    return app.test_client(use_cookies=False)


@pytest.fixture(scope='session')
def db(app):
    with app.app_context():
        yield _db


# ─────────────────────────────────────────────────────────────────────────────
# Seed data
# ─────────────────────────────────────────────────────────────────────────────

def _seed_test_data(app):
    with app.app_context():
        for role_name in ['owner', 'manager', 'staff', 'customer']:
            if not Role.query.filter_by(name=role_name).first():
                _db.session.add(Role(name=role_name))
        _db.session.commit()

        # Owner
        _create_user('test_owner', 'owner@test.com', 'Test@1234', 'owner')

        # Manager + profile
        mgr_user = _create_user('test_manager', 'mgr@test.com', 'Test@1234', 'manager')
        if not _db.session.get(Manager, mgr_user.id):
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

        # Staff + profile
        stf_user = _create_user('test_staff', 'staff@test.com', 'Test@1234', 'staff')
        if not _db.session.get(Staff, stf_user.id):
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

        # Dedicated user for password-change tests (never shared with other flows)
        pwd_user = _create_user('test_pwd_user', 'pwd@test.com', 'Test@1234', 'staff')
        if not _db.session.get(Staff, pwd_user.id):
            _db.session.add(Staff(
                staff_id=pwd_user.id,
                staff_name='Pwd Test Stylist',
                staff_contact='+91-9000000010',
                staff_email='pwd@test.com',
                staff_skills='Haircut',
                staff_role='Stylist',
                staff_dob=date(1996, 1, 1),
                staff_doj=date(2023, 6, 1),
                staff_salary=25000,
            ))
        _db.session.commit()

        # Customer + profile
        cust_user = _create_user('test_customer', 'cust@test.com', 'Test@1234', 'customer')
        if not _db.session.get(Customer, cust_user.id):
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

        # Service
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

        # Product
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
# Token fixtures
# ─────────────────────────────────────────────────────────────────────────────

def _login(client, endpoint, username, password):
    rv = client.post(endpoint,
                     json={'username': username, 'password': password},
                     content_type='application/json')
    assert rv.status_code == 200, f"Login failed for {username!r}: {rv.get_json()}"
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


@pytest.fixture(scope='session')
def pwd_user_token(client):
    """Dedicated token for password-change tests — not shared with other suites."""
    return _login(client, '/staff-login', 'test_pwd_user', 'Test@1234')


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def auth_headers(token):
    return {
        'Authorization': f'Bearer {token}',
        'Authentication-Token': token,
        'Content-Type': 'application/json',
    }
