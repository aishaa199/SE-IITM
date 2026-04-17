"""
test_salonstatistics.py – Tests for SalonDailyAppointmentCountResource (/api/daily-appointment-count).

Endpoints covered:
  GET /api/daily-appointment-count
"""
import pytest
from tests.conftest import auth_headers

class TestSalonDailyCountResource:
    """Tests for manager-only salon statistics."""

    def test_get_daily_counts_success(self, client, manager_token):
        """TC-STAT-01: Manager can retrieve daily appointment counts."""
        rv = client.get('/api/daily-appointment-count', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        # Even if 0, it should be a list.
        if len(data) > 0:
            assert 'date' in data[0]
            assert 'count' in data[0]

    def test_get_daily_counts_forbidden_for_staff(self, client, staff_token):
        """TC-STAT-02: Staff member cannot access daily-appointment-count."""
        rv = client.get('/api/daily-appointment-count', headers=auth_headers(staff_token))
        assert rv.status_code == 403

    def test_get_daily_counts_forbidden_for_customer(self, client, customer_token):
        """TC-STAT-03: Customer cannot access daily-appointment-count."""
        rv = client.get('/api/daily-appointment-count', headers=auth_headers(customer_token))
        assert rv.status_code == 403

    def test_get_daily_counts_unauthenticated(self, client):
        """TC-STAT-04: No token → 401/302."""
        rv = client.get('/api/daily-appointment-count')
        assert rv.status_code in (401, 302)
