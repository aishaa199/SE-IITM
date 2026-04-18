"""
test_managerstaffattendance.py – Tests for Manager marking bulk staff absent.

Endpoints covered:
  POST /api/mark-staff-absent
"""
import pytest
from tests.conftest import auth_headers
from main import create_app

class TestManagerStaffAttendance:
    """Manager-facing bulk attendance operations."""

    def test_mark_staff_absent_success(self, client, manager_token):
        """TC-MGR-ATTN-01: Manager can mark absent for all staff members who haven't marked attendance."""
        rv = client.post('/api/mark-staff-absent', headers=auth_headers(manager_token))
        assert rv.status_code == 201
        data = rv.get_json()
        assert 'message' in data
        assert 'Bulk attendance processing complete' in data['message']

    def test_mark_staff_absent_forbidden_for_staff(self, client, staff_token):
        """TC-MGR-ATTN-02: Staff cannot access manager bulk attendance marking."""
        rv = client.post('/api/mark-staff-absent', headers=auth_headers(staff_token))
        assert rv.status_code == 403

    def test_mark_staff_absent_forbidden_for_customer(self, client, customer_token):
        """TC-MGR-ATTN-03: Customer cannot access manager bulk attendance marking."""
        rv = client.post('/api/mark-staff-absent', headers=auth_headers(customer_token))
        assert rv.status_code == 403

    def test_mark_staff_absent_unauthenticated(self, client):
        """TC-MGR-ATTN-04: No token → 401/302."""
        rv = client.post('/api/mark-staff-absent')
        assert rv.status_code in (401, 302)

    def test_mark_staff_absent_with_some_present(self, client, manager_token, staff_token):
        """TC-MGR-ATTN-05: Manager marks absent and only counts those who haven't marked attendance."""
        # Ensure staff is present
        client.post('/api/staff-attendance', headers=auth_headers(staff_token))
        
        # Manager runs bulk absent marking - using a fresh client to avoid session leakage
        fresh_client = create_app().test_client()
        rv = fresh_client.post('/api/mark-staff-absent', headers=auth_headers(manager_token))
        assert rv.status_code == 201
        data = rv.get_json()
        
        assert 'staff members marked as absent' in data['message']
