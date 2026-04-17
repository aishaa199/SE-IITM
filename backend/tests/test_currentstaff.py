"""
test_currentstaff.py – Tests for CurrentStaffResource (/api/staff-info).

Endpoints covered:
  GET /api/staff-info
  PUT /api/staff-info
"""
import pytest
from tests.conftest import auth_headers

class TestCurrentStaffResource:
    """Tests for logged-in staff profile management."""

    def test_get_staff_info_success(self, client, staff_token):
        """TC-STF-INFO-01: Logged-in staff can retrieve their own profile."""
        rv = client.get('/api/staff-info', headers=auth_headers(staff_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert 'staff_email' in data
        assert 'staff_name' in data
        assert data['staff_email'] == 'staff@test.com'

    def test_get_staff_info_forbidden_for_customer(self, client, customer_token):
        """TC-STF-INFO-02: Customer cannot access staff-info endpoint."""
        rv = client.get('/api/staff-info', headers=auth_headers(customer_token))
        assert rv.status_code == 403

    def test_get_staff_info_unauthenticated(self, client):
        """TC-STF-INFO-03: No token → 401/302."""
        rv = client.get('/api/staff-info')
        assert rv.status_code in (401, 302)

    def test_update_staff_info_success(self, client, staff_token):
        """TC-STF-INFO-04: Staff can update their own profile fields (e.g. contact)."""
        new_contact = "+91-9999999999"
        rv = client.put('/api/staff-info', 
                        headers=auth_headers(staff_token),
                        json={'staff_contact': new_contact})
        assert rv.status_code == 200
        data = rv.get_json()
        assert "Profile updated successfully" in data['message']
        
        # Verify changes via GET
        get_rv = client.get('/api/staff-info', headers=auth_headers(staff_token))
        assert get_rv.get_json()['staff_contact'] == new_contact

    def test_update_staff_info_unauthorized(self, client, manager_token):
        """TC-STF-INFO-05: Manager cannot update info via this staff-only endpoint."""
        rv = client.put('/api/staff-info', 
                        headers=auth_headers(manager_token),
                        json={'staff_name': 'Hacker'})
        assert rv.status_code == 403
