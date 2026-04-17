"""
test_currentcustomer.py – Tests for CurrentCustomerResource (/api/customer-info).

Endpoints covered:
  GET /api/customer-info
  PUT /api/customer-info
"""
import pytest
from tests.conftest import auth_headers

class TestCurrentCustomerResource:
    """Tests for logged-in customer profile management."""

    def test_get_customer_info_success(self, client, customer_token):
        """TC-CUST-INFO-01: Logged-in customer can retrieve their profile."""
        rv = client.get('/api/customer-info', headers=auth_headers(customer_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert 'customer_email' in data
        assert 'customer_name' in data
        assert data['customer_email'] == 'cust@test.com'

    def test_get_customer_info_forbidden_for_staff(self, client, staff_token):
        """TC-CUST-INFO-02: Staff member cannot access customer-info endpoint."""
        rv = client.get('/api/customer-info', headers=auth_headers(staff_token))
        assert rv.status_code == 403

    def test_get_customer_info_unauthenticated(self, client):
        """TC-CUST-INFO-03: No token → 401/302."""
        rv = client.get('/api/customer-info')
        assert rv.status_code in (401, 302)

    def test_update_customer_info_success(self, client, customer_token):
        """TC-CUST-INFO-04: Customer can update their profile fields (e.g. contact)."""
        new_contact = "+91-8888888888"
        new_address = "123 Updated Street, City"
        payload = {
            'customer_contact': new_contact,
            'customer_address': new_address
        }
        rv = client.put('/api/customer-info', 
                        headers=auth_headers(customer_token),
                        json=payload)
        assert rv.status_code == 200
        data = rv.get_json()
        assert "Profile updated successfully" in data['message']
        
        # Verify changes via GET
        get_rv = client.get('/api/customer-info', headers=auth_headers(customer_token))
        fetched_data = get_rv.get_json()
        assert fetched_data['customer_contact'] == new_contact
        assert fetched_data['customer_address'] == new_address

    def test_update_customer_info_unauthorized(self, client, manager_token):
        """TC-CUST-INFO-05: Manager cannot update info via this customer-only endpoint."""
        rv = client.put('/api/customer-info', 
                        headers=auth_headers(manager_token),
                        json={'customer_name': 'Hacker'})
        assert rv.status_code == 403
