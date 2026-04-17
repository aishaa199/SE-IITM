"""
test_staffdashboard.py – Tests for StaffDashboard (/api/staff-dashboard).

Endpoints covered:
  GET /api/staff-dashboard
"""
import pytest
from tests.conftest import auth_headers

class TestStaffDashboard:
    """Tests for the staff dashboard statistics."""

    def test_get_staff_dashboard_success(self, client, staff_token):
        """TC-STF-DASH-01: Logged-in staff can retrieve their dashboard statistics."""
        rv = client.get('/api/staff-dashboard', headers=auth_headers(staff_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert 'total_appointments_today' in data
        assert 'completed_appointments_today' in data
        assert isinstance(data['total_appointments_today'], int)
        assert isinstance(data['completed_appointments_today'], int)

    def test_get_staff_dashboard_forbidden_for_manager(self, client, manager_token):
        """TC-STF-DASH-02: Manager cannot access the staff-specific dashboard."""
        rv = client.get('/api/staff-dashboard', headers=auth_headers(manager_token))
        assert rv.status_code == 403

    def test_get_staff_dashboard_forbidden_for_customer(self, client, customer_token):
        """TC-STF-DASH-03: Customer cannot access the staff-specific dashboard."""
        rv = client.get('/api/staff-dashboard', headers=auth_headers(customer_token))
        assert rv.status_code == 403

    def test_get_staff_dashboard_unauthenticated(self, client):
        """TC-STF-DASH-04: No token → 401/302."""
        rv = client.get('/api/staff-dashboard')
        assert rv.status_code in (401, 302)
