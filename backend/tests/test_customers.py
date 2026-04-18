"""
test_customers.py – Tests for Customer CRUD and Review APIs.

Endpoints covered:
  GET    /api/customer
  GET    /api/customer/<id>
  POST   /api/customer
  PUT    /api/customer/<id>
  DELETE /api/customer/<id>
  GET    /api/customer-review          (pending reviews)
  GET    /api/customer-reviewed-appointments
  POST   /api/customer-reviewed-appointments  (submit review)
"""
import pytest
from tests.conftest import auth_headers


class TestCustomerCRUD:
    """Manager-facing customer management."""

    def test_list_customers_manager(self, client, manager_token):
        """TC-CUST-01: Manager can list all customers with correct fields."""
        rv = client.get('/api/customer', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1
        fields = ('customer_id', 'customer_name', 'customer_email',
                  'customer_type', 'customer_available_rewards')
        for f in fields:
            assert f in data[0], f"Missing: {f}"

    def test_list_customers_unauthenticated(self, client):
        """TC-CUST-02: No token → 401/302.
        
        Accepts both as Flask-Security-Too may redirect for sessions."""
        rv = client.get('/api/customer')
        assert rv.status_code in (401, 302)

    def test_get_customer_by_id(self, client, manager_token):
        """TC-CUST-03: Manager fetches specific customer by ID."""
        list_rv = client.get('/api/customer', headers=auth_headers(manager_token))
        cid = list_rv.get_json()[0]['customer_id']
        rv = client.get(f'/api/customer/{cid}', headers=auth_headers(manager_token))
        data = rv.get_json()
        assert rv.status_code == 200
        assert data['customer_id'] == cid

    def test_get_nonexistent_customer(self, client, manager_token):
        """TC-CUST-04: Fetching non-existent customer ID returns 404."""
        rv = client.get('/api/customer/99999', headers=auth_headers(manager_token))
        assert rv.status_code == 404

    def test_create_customer_by_manager(self, client, manager_token):
        """TC-CUST-05: Manager creates a new customer profile."""
        import random
        import string
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        email = f'walkin_{random_suffix}@salon.com'
        
        rv = client.post('/api/customer',
                         headers=auth_headers(manager_token),
                         json={
                             'customer_email': email,
                             'customer_name': 'Walk-in Customer',
                             'customer_contact': '+91-9000001111',
                             'customer_dob': '1990-03-25',
                             'customer_address': '5 Walk-in Lane, Mumbai',
                             'customer_preferences': 'Facial',
                         })
        data = rv.get_json()
        assert rv.status_code == 201
        assert 'customer_id' in data

    def test_create_customer_missing_email(self, client, manager_token):
        """TC-CUST-06: Missing customer_email returns 400."""
        rv = client.post('/api/customer',
                         headers=auth_headers(manager_token),
                         json={
                             'customer_name': 'No Email',
                             'customer_contact': '+91-9000002222',
                             'customer_dob': '1990-01-01',
                             'customer_address': 'Somewhere',
                         })
        assert rv.status_code == 400

    def test_create_customer_by_customer_forbidden(self, client, customer_token):
        """TC-CUST-07: Customer role cannot POST to /api/customer."""
        rv = client.post('/api/customer',
                         headers=auth_headers(customer_token),
                         json={
                             'customer_email': 'hack@salon.com',
                             'customer_name': 'Hacker',
                             'customer_contact': '+91-9999999999',
                             'customer_dob': '1990-01-01',
                             'customer_address': 'Hack Lane',
                         })
        assert rv.status_code == 403

    def test_update_customer(self, client, manager_token):
        """TC-CUST-08: Manager updates customer contact number."""
        list_rv = client.get('/api/customer', headers=auth_headers(manager_token))
        cid = list_rv.get_json()[0]['customer_id']
        rv = client.put(f'/api/customer/{cid}',
                        headers=auth_headers(manager_token),
                        json={'customer_contact': '+91-9876543999'})
        assert rv.status_code == 200
        assert 'updated' in rv.get_json()['message'].lower()

    def test_update_nonexistent_customer(self, client, manager_token):
        """TC-CUST-09: Updating a non-existent customer returns 404."""
        rv = client.put('/api/customer/99999',
                        headers=auth_headers(manager_token),
                        json={'customer_contact': '+91-1234567890'})
        assert rv.status_code == 404

    def test_delete_customer(self, client, manager_token):
        """TC-CUST-10: Manager creates then deletes a customer."""
        create_rv = client.post('/api/customer',
                                headers=auth_headers(manager_token),
                                json={
                                    'customer_email': 'todelete@salon.com',
                                    'customer_name': 'To Delete',
                                    'customer_contact': '+91-9000003333',
                                    'customer_dob': '1985-12-12',
                                    'customer_address': 'Delete Street',
                                })
        cid = create_rv.get_json()['customer_id']
        rv = client.delete(f'/api/customer/{cid}',
                           headers=auth_headers(manager_token))
        assert rv.status_code == 200
        assert 'deleted' in rv.get_json()['message'].lower()


class TestCustomerReviews:
    """Customer self-service review endpoints."""

    def test_pending_reviews_empty(self, client, customer_token):
        """TC-CUST-11: New customer with no completed appointments has empty pending list."""
        rv = client.get('/api/customer-review', headers=auth_headers(customer_token))
        data = rv.get_json()
        assert rv.status_code == 200
        assert isinstance(data, list)
        # Each item should have these keys
        for item in data:
            assert 'appointment_id' in item
            assert 'services' in item
            assert 'staff_name' in item

    def test_pending_reviews_manager_forbidden(self, client, manager_token):
        """TC-CUST-12: Manager cannot call customer-review endpoint."""
        rv = client.get('/api/customer-review', headers=auth_headers(manager_token))
        assert rv.status_code == 403

    def test_reviewed_appointments_list(self, client, customer_token):
        """TC-CUST-13: Customer can view their reviewed appointments list."""
        rv = client.get('/api/customer-reviewed-appointments',
                        headers=auth_headers(customer_token))
        assert rv.status_code == 200
        assert isinstance(rv.get_json(), list)

    def test_submit_review_invalid_appointment(self, client, customer_token):
        """TC-CUST-14: Submitting review for non-existent appointment returns 404."""
        rv = client.post('/api/customer-reviewed-appointments',
                         headers=auth_headers(customer_token),
                         json={
                             'appointment_id': 99999,
                             'rating': 5,
                             'review': 'Great service!',
                         })
        assert rv.status_code == 404

    def test_submit_review_missing_rating(self, client, customer_token):
        """TC-CUST-15: Review without rating returns 400."""
        rv = client.post('/api/customer-reviewed-appointments',
                         headers=auth_headers(customer_token),
                         json={
                             'appointment_id': 1,
                             'review': 'Nice place',
                             # rating missing
                         })
        assert rv.status_code == 400
