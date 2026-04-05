"""
test_managerstaffattendance.py – Tests for Manager viewing staff attendance.

Endpoints covered:
  GET  /api/manager-staff-attendance
"""
import pytest
from tests.conftest import auth_headers
from datetime import date

class TestManagerStaffAttendance:
    """Manager-facing attendance overview."""

    def test_list_attendance_today_manager(self, client, manager_token, staff_token):
        """TC-MAR-ATTN-01: Manager can list today's attendance records with correct fields."""
        # Mark attendance first using staff account
        client.post('/api/staff-attendance', headers=auth_headers(staff_token))
        
        rv = client.get('/api/manager-staff-attendance', headers=auth_headers(manager_token))
        # Note: If this fails with 403, it's likely a roles_required vs roles_accepted issue 
        # in the backend for manager-level access.
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        fields = ('register_id', 'staff_id', 'register_datetime')
        for f in fields:
            assert f in data[0], f"Missing: {f}"

    def test_list_attendance_unauthenticated(self, client):
        """TC-MAR-ATTN-02: No token → 302/401."""
        rv = client.get('/api/manager-staff-attendance')
        assert rv.status_code in (302, 401)

    def test_list_attendance_by_date_manager(self, client, manager_token, staff_token):
        """TC-MAR-ATTN-03: Manager can list attendance for a specific date."""
        # Mark attendance for today
        client.post('/api/staff-attendance', headers=auth_headers(staff_token))
        today_str = date.today().strftime('%Y-%m-%d')
        
        rv = client.get(f'/api/manager-staff-attendance?date={today_str}', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_list_attendance_invalid_date_format(self, client, manager_token):
        """TC-MAR-ATTN-04: Invalid date format returns 400."""
        rv = client.get('/api/manager-staff-attendance?date=05/04/2026', headers=auth_headers(manager_token))
        assert rv.status_code == 400

    def test_list_attendance_no_records(self, client, manager_token):
        """TC-MAR-ATTN-05: Manager fetching date with no records returns 404."""
        rv = client.get('/api/manager-staff-attendance?date=1999-01-01', headers=auth_headers(manager_token))
        assert rv.status_code == 404

    def test_list_attendance_staff_forbidden(self, client, staff_token):
        """TC-MAR-ATTN-06: Staff role cannot access manager attendance view."""
        rv = client.get('/api/manager-staff-attendance', headers=auth_headers(staff_token))
        assert rv.status_code == 403
