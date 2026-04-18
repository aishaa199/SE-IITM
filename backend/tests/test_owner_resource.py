"""
test_owner_resource.py – Tests for Owner resource (/api/create-manager).

Endpoints covered:
  POST /api/create-manager (Create Manager)
"""
import pytest
from tests.conftest import auth_headers

class TestOwnerResource:
    """Tests for owner activities like manager creation."""

    def test_create_manager_success(self, client, owner_token):
        """TC-OWN-01: Owner can successfully create a new manager."""
        payload = {
            'fullname': 'New Manager',
            'email': 'newmgr1@test.com',
            'phone': '1234567890',
            'skills': 'Management',
            'role': 'Store Manager',
            'dob': '1990-01-01',
            'doj': '2023-01-01',
            'branch_name': 'Downtown',
            'username': 'unique_mgr_user1',
            'password': 'password123'
        }
        rv = client.post('/api/create-manager', 
                         headers=auth_headers(owner_token),
                         json=payload)
        assert rv.status_code == 200
        assert "Manager created successfully" in rv.get_json()['message']

    def test_create_manager_duplicate_username(self, client, owner_token):
        """TC-OWN-02: Returns 400 for duplicate username."""
        # Use an existing username (manager exists from dummy data)
        payload = {
            'username': 'manager', 
            'password': 'password123',
            'branch_name': 'Downtown' # Included to avoid IntegrityError if duplication check is skipped
        }
        rv = client.post('/api/create-manager', 
                         headers=auth_headers(owner_token),
                         json=payload)
        assert rv.status_code == 400
        assert "User with this username already exists" in rv.get_json()['message']

    def test_create_manager_missing_username(self, client, owner_token):
        """TC-OWN-03: Returns 400 if username is missing."""
        rv = client.post('/api/create-manager', 
                         headers=auth_headers(owner_token),
                         json={'password': 'pass', 'branch_name': 'Downtown'})
        assert rv.status_code == 400
        assert "username not provided" in rv.get_json()['message']

    def test_owner_resource_forbidden_for_manager(self, client, manager_token):
        """TC-OWN-04: Manager cannot create another manager via this endpoint."""
        rv = client.post('/api/create-manager', 
                         headers=auth_headers(manager_token),
                         json={})
        assert rv.status_code == 403

    def test_owner_resource_unauthenticated(self, client):
        """TC-OWN-05: No token -> 401/302."""
        rv = client.post('/api/create-manager', json={})
        assert rv.status_code in (401, 302)
