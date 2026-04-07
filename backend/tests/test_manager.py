import pytest
from tests.conftest import auth_headers

def _get_first_manager_id(client, token):
    rv = client.get('/api/manager', headers=auth_headers(token))
    data = rv.get_json()
    return data[0]['manager_id'] if data else None

class TestManagerCRUD:
    """Tests for Manager Account and Profile Management."""

    def test_create_manager_success(self, client, owner_token):
        """TC-MGR-01: Owner creates a new manager account."""
        payload = {
            "username": "new_branch_mgr",
            "email": "new_mgr@salon.com",
            "password": "Password@123",
            "manager_name": "New Manager",
            "manager_contact": "+91-9876543210",
            "branch_name": "North Branch"
        }
        rv = client.post('/api/create-manager', 
                         json=payload, 
                         headers=auth_headers(owner_token))
        
        assert rv.status_code == 201
        assert "Manager created" in rv.get_json()['message']
        assert rv.get_json()['username'] == "new_branch_mgr"

    def test_create_manager_forbidden_for_staff(self, client, staff_token):
        """TC-MGR-02: Staff cannot create managers."""
        rv = client.post('/api/create-manager', 
                         json={}, 
                         headers=auth_headers(staff_token))
        # Flask-Security returns 403 for role failure
        assert rv.status_code == 403

    def test_list_managers_owner(self, client, owner_token):
        """TC-MGR-03: Owner can view all managers."""
        rv = client.get('/api/manager', headers=auth_headers(owner_token))
        assert rv.status_code == 200
        assert isinstance(rv.get_json(), list)
        assert len(rv.get_json()) >= 1

    def test_get_specific_manager(self, client, owner_token):
        """TC-MGR-04: Fetch manager details by ID."""
        mid = _get_first_manager_id(client, owner_token)
        rv = client.get(f'/api/manager/{mid}', headers=auth_headers(owner_token))
        
        assert rv.status_code == 200
        data = rv.get_json()
        assert data['manager_id'] == mid
        assert 'manager_name' in data

    def test_update_manager_profile(self, client, manager_token, owner_token):
        """TC-MGR-05: Manager/Owner can update profile details."""
        mid = _get_first_manager_id(client, owner_token)
        payload = {
            "manager_name": "Updated Name",
            "manager_skills": "Advanced Styling, Inventory",
            "branch_name": "Main Branch HQ"
        }
        rv = client.put(f'/api/manager/{mid}', 
                        json=payload, 
                        headers=auth_headers(manager_token))
        
        assert rv.status_code == 200
        assert "updated" in rv.get_json()['message'].lower()

    def test_delete_manager_owner_only(self, client, owner_token, manager_token):
        """TC-MGR-06: Owner can delete; Manager cannot delete self/others."""
        mid = _get_first_manager_id(client, owner_token)
        
        # 1. Try deleting as manager (should be forbidden)
        fail_rv = client.delete(f'/api/manager/{mid}', headers=auth_headers(manager_token))
        assert fail_rv.status_code == 403
        
        # 2. Delete as owner
        success_rv = client.delete(f'/api/manager/{mid}', headers=auth_headers(owner_token))
        assert success_rv.status_code == 200
        assert "deleted" in success_rv.get_json()['message'].lower()

    def test_manager_not_found(self, client, owner_token):
        """TC-MGR-07: 404 for non-existent manager ID."""
        rv = client.get('/api/manager/99999', headers=auth_headers(owner_token))
        assert rv.status_code == 404