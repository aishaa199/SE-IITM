"""
test_changepassword.py – Tests for Change Password functionality.

Uses a dedicated test_pwd_user account so that password mutations
never affect staff_token (shared by many other test suites).

Endpoint:
  PUT /api/change-password
"""
import pytest
from tests.conftest import auth_headers


class TestChangePasswordAPI:

    def test_change_password_mismatch(self, client, pwd_user_token):
        """TC-PWD-01: New password ≠ confirm password → 400."""
        rv = client.put('/api/change-password',
                        json={
                            'current_password': 'Test@1234',
                            'new_password': 'NewPass@1234',
                            'confirm_password': 'DifferentPass@1234',
                        },
                        headers=auth_headers(pwd_user_token))
        assert rv.status_code == 400
        assert rv.get_json()['message'] == 'New password and confirm password do not match'

    def test_change_password_same_as_current(self, client, pwd_user_token):
        """TC-PWD-02: New password identical to current → 400."""
        rv = client.put('/api/change-password',
                        json={
                            'current_password': 'Test@1234',
                            'new_password': 'Test@1234',
                            'confirm_password': 'Test@1234',
                        },
                        headers=auth_headers(pwd_user_token))
        assert rv.status_code == 400
        assert rv.get_json()['message'] == 'New password cannot be the same as the current password'

    def test_change_password_empty_new_password(self, client, pwd_user_token):
        """TC-PWD-03: Empty new_password → 400."""
        rv = client.put('/api/change-password',
                        json={
                            'current_password': 'Test@1234',
                            'new_password': '',
                            'confirm_password': '',
                        },
                        headers=auth_headers(pwd_user_token))
        assert rv.status_code == 400
        assert rv.get_json()['message'] == 'New password and confirm password cannot be empty'

    def test_change_password_wrong_current(self, client, pwd_user_token):
        """TC-PWD-04: Wrong current password → 400."""
        rv = client.put('/api/change-password',
                        json={
                            'current_password': 'WrongPassword',
                            'new_password': 'NewPass@1234',
                            'confirm_password': 'NewPass@1234',
                        },
                        headers=auth_headers(pwd_user_token))
        assert rv.status_code == 400
        assert rv.get_json()['message'] == 'Wrong current password'

    def test_change_password_unauthenticated(self, client):
        """TC-PWD-05: No token → 401/302."""
        rv = client.put('/api/change-password', json={})
        assert rv.status_code in (302, 401)

    def test_change_password_success(self, client, pwd_user_token):
        """TC-PWD-06: Valid current password and matching new passwords → 200.
        Run last so token invalidation does not affect preceding tests.
        """
        rv = client.put('/api/change-password',
                        json={
                            'current_password': 'Test@1234',
                            'new_password': 'NewPwd@5678',
                            'confirm_password': 'NewPwd@5678',
                        },
                        headers=auth_headers(pwd_user_token))
        assert rv.status_code == 200
        assert rv.get_json()['message'] == 'Password changed successfully'
