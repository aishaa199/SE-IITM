import pytest
from tests.conftest import auth_headers

class TestChangePasswordAPI:
    """Tests for the /api/change-password endpoint."""

    @pytest.mark.parametrize("user_type, username", [
        ("owner", "test_owner"),
        ("manager", "test_manager"),
        ("staff", "test_staff"),
        ("customer", "test_customer"),
    ])
    def test_change_password_success(self, client, user_type, username):
        """TC-CP-01: Successfully change password for any role."""
        # 1. Login to get a FRESH token
        login_rv = client.post(f"/{user_type}-login", json={
            "username": username,
            "password": "Test@1234"
        })
        assert login_rv.status_code == 200, f"Login failed for {username}: {login_rv.get_json()}"
        token = login_rv.get_json()["token"]

        # 2. Change password
        payload = {
            "current_password": "Test@1234",
            "new_password": "NewPassword@123",
            "confirm_password": "NewPassword@123"
        }
        
        # Using the specific header required by Flask-Security-Too
        rv = client.put("/api/change-password", 
                         headers={"Authentication-Token": token},
                         json=payload)
        
        assert rv.status_code == 200
        assert "Password changed successfully" in rv.get_json()["message"]

    def test_change_password_wrong_current(self, client, owner_token):
        """TC-CP-02: Fail when current password is incorrect."""
        payload = {
            "current_password": "WrongPassword",
            "new_password": "NewPassword@123",
            "confirm_password": "NewPassword@123"
        }
        rv = client.put("/api/change-password", 
                         headers={"Authentication-Token": owner_token},
                         json=payload)
        assert rv.status_code == 400
        assert "Wrong current password" in rv.get_json()["message"]

    def test_change_password_mismatch(self, client, owner_token):
        """TC-CP-03: Fail when new and confirm passwords do not match."""
        payload = {
            "current_password": "Test@1234",
            "new_password": "NewPassword1",
            "confirm_password": "NewPassword2"
        }
        rv = client.put("/api/change-password", 
                         headers={"Authentication-Token": owner_token},
                         json=payload)
        assert rv.status_code == 400
        assert "not match" in rv.get_json()["message"]

    def test_change_password_unauthenticated(self, client):
        """TC-CP-04: Fail when no token is provided."""
        rv = client.put("/api/change-password", json={})
        assert rv.status_code == 401
