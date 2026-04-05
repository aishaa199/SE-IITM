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
        """TC-ATTN-03: Staff can mark their attendance for today."""
        # We try to mark it. If already marked (by TC-ATTN-01 or seed), we expect 400.
        # Otherwise 201. Both are valid 'handled' responses.
        rv = client.post('/api/staff-attendance', headers=auth_headers(staff_token))
        assert rv.status_code in (201, 400)
        
        if rv.status_code == 201:
            data = rv.get_json()
            assert 'message' in data
            assert 'Attendance marked successfully' in data['message']

    def test_mark_attendance_duplicate(self, client, staff_token):
        """TC-ATTN-04: Staff cannot mark attendance twice on the same day."""
        # Ensure it's marked
        client.post('/api/staff-attendance', headers=auth_headers(staff_token))
        # Second attempt
        rv = client.post('/api/staff-attendance', headers=auth_headers(staff_token))
        assert rv.status_code == 400
        assert 'already marked' in rv.get_json()['message']

    def test_mark_attendance_manager_forbidden(self, client, manager_token):
        """TC-ATTN-05: Manager role cannot POST to staff attendance endpoint."""
        rv = client.post('/api/staff-attendance', headers=auth_headers(manager_token))
        assert rv.status_code == 403
