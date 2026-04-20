"""
test_staffattendance.py – Tests for Staff marking and viewing their attendance.

Endpoints covered:
  GET  /api/staff-attendance
  POST /api/staff-attendance
"""
import pytest
from tests.conftest import auth_headers

class TestStaffAttendance:
    """Staff-facing attendance operations."""

    def test_get_staff_attendance_own(self, client, staff_token):
        """TC-ATTN-01: Staff can view their own attendance records with correct fields."""
        # Mark attendance first to ensure record exists
        client.post('/api/staff-attendance', headers=auth_headers(staff_token))
        
        rv = client.get('/api/staff-attendance', headers=auth_headers(staff_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        fields = ('register_id', 'staff_id', 'register_datetime')
        for f in fields:
            assert f in data[0], f"Missing: {f}"

    def test_get_staff_attendance_unauthenticated(self, client):
        """TC-ATTN-02: No token → 302/401."""
        rv = client.get('/api/staff-attendance')
        assert rv.status_code in (302, 401)

    def test_mark_attendance_staff(self, client, staff_token):
        """TC-ATTN-03: Staff marks attendance – 201 first time, 409 if already marked."""
        rv = client.post('/api/staff-attendance', headers=auth_headers(staff_token))
        assert rv.status_code in (201, 409)

        if rv.status_code == 201:
            assert 'message' in rv.get_json()

    def test_mark_attendance_duplicate(self, client, staff_token):
        """TC-ATTN-04: Staff cannot mark attendance twice on the same day – 409 Conflict."""
        client.post('/api/staff-attendance', headers=auth_headers(staff_token))
        rv = client.post('/api/staff-attendance', headers=auth_headers(staff_token))
        assert rv.status_code == 409
        assert 'already' in rv.get_json()['message'].lower()

    def test_mark_attendance_manager_forbidden(self, client, manager_token):
        """TC-ATTN-05: Manager role cannot POST to staff attendance endpoint."""
        rv = client.post('/api/staff-attendance', headers=auth_headers(manager_token))
        assert rv.status_code == 403
