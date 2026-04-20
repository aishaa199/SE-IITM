"""
test_managerstaffattendance.py – Tests for Manager viewing staff attendance.

NOTE: Each test uses ONLY manager_token to avoid SQLAlchemy scoped-session
cross-request state when mixing different role tokens in the same function.
Attendance data is created by earlier test_staffattendance.py tests.

Endpoint covered:
  GET  /api/manager-staff-attendance
"""
import pytest
from tests.conftest import auth_headers
from datetime import date


class TestManagerStaffAttendance:

    def test_list_attendance_today_manager(self, client, manager_token):
        """TC-MAR-ATTN-01: Manager lists today's attendance – 200 with records or 404 if none."""
        rv = client.get('/api/manager-staff-attendance', headers=auth_headers(manager_token))
        # 200 when records exist (from earlier attendance tests), 404 when empty
        assert rv.status_code in (200, 404)
        if rv.status_code == 200:
            data = rv.get_json()
            assert isinstance(data, list)
            assert len(data) >= 1
            for field in ('register_id', 'staff_id', 'register_datetime'):
                assert field in data[0], f"Missing: {field}"

    def test_list_attendance_unauthenticated(self, client):
        """TC-MAR-ATTN-02: No token → 302/401."""
        rv = client.get('/api/manager-staff-attendance')
        assert rv.status_code in (302, 401)

    def test_list_attendance_by_date_today_manager(self, client, manager_token):
        """TC-MAR-ATTN-03: Manager lists attendance for today by explicit date."""
        today_str = date.today().strftime('%Y-%m-%d')
        rv = client.get(f'/api/manager-staff-attendance?date={today_str}',
                        headers=auth_headers(manager_token))
        assert rv.status_code in (200, 404)
        if rv.status_code == 200:
            assert isinstance(rv.get_json(), list)

    def test_list_attendance_invalid_date_format(self, client, manager_token):
        """TC-MAR-ATTN-04: Invalid date format returns 400."""
        rv = client.get('/api/manager-staff-attendance?date=05/04/2026',
                        headers=auth_headers(manager_token))
        assert rv.status_code == 400

    def test_list_attendance_no_records(self, client, manager_token):
        """TC-MAR-ATTN-05: Date with no records → 404."""
        rv = client.get('/api/manager-staff-attendance?date=1999-01-01',
                        headers=auth_headers(manager_token))
        assert rv.status_code == 404

    def test_list_attendance_staff_forbidden(self, client, staff_token):
        """TC-MAR-ATTN-06: Staff role cannot access manager attendance view – 403."""
        rv = client.get('/api/manager-staff-attendance', headers=auth_headers(staff_token))
        assert rv.status_code == 403
