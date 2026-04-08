"""
test_changepassword.py – Tests for Change Password functionality.

Endpoints:
  PUT /api/change-password
"""
import pytest
from tests.conftest import auth_headers

class TestChangePasswordAPI:
    """Standardized ChangePassword API Tests."""

    def test_change_password_success(self, client, staff_token):
        """TC-PWD-01: User can change their password with correct current password."""
        payload = {
            "current_password": "Test@1234",
            "new_password": "NewStaff@1234",
            "confirm_password": "NewStaff@1234"
        }
        rv = client.put('/api/change-password', json=payload, headers=auth_headers(staff_token))
        assert rv.status_code == 200
        assert rv.get_json()['message'] == "Password changed successfully"

    def test_change_password_wrong_current(self, client, staff_token):
        """TC-PWD-02: Changing password with wrong current password returns 400."""
        payload = {
            "current_password": "WrongPassword",
            "new_password": "NewStaff@1234",
            "confirm_password": "NewStaff@1234"
        }
        rv = client.put('/api/change-password', json=payload, headers=auth_headers(staff_token))
        assert rv.status_code == 400
        assert rv.get_json()['message'] == "Wrong current password"

    def test_change_password_mismatch(self, client, staff_token):
        """TC-PWD-03: New password and confirm password mismatch returns 400."""
        payload = {
            "current_password": "Test@1234",
            "new_password": "NewStaff@1234",
            "confirm_password": "DifferentPassword"
        }
        rv = client.put('/api/change-password', json=payload, headers=auth_headers(staff_token))
        assert rv.status_code == 400
        assert rv.get_json()['message'] == "New password and confirm password do not match"

    def test_change_password_same_as_current(self, client, staff_token):
        """TC-PWD-04: New password same as current returns 400."""
        payload = {
            "current_password": "Test@1234",
            "new_password": "Test@1234",
            "confirm_password": "Test@1234"
        }
        rv = client.put('/api/change-password', json=payload, headers=auth_headers(staff_token))
        assert rv.status_code == 400
        assert rv.get_json()['message'] == "New password cannot be the same as the current password"

    def test_change_password_empty_fields(self, client, staff_token):
        """TC-PWD-05: Empty password fields return 400."""
        payload = {
            "current_password": "Test@1234",
            "new_password": "",
            "confirm_password": ""
        }
        rv = client.put('/api/change-password', json=payload, headers=auth_headers(staff_token))
        assert rv.status_code == 400
        assert rv.get_json()['message'] == "New password and confirm password cannot be empty"

    def test_change_password_unauthenticated(self, client):
        """TC-PWD-06: No token → 302/401."""
        rv = client.put('/api/change-password', json={})
        assert rv.status_code in (302, 401)
