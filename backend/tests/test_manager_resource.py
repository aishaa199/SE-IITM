"""
test_manager_resource.py – Tests for ManagerResource (/api/manager).

Endpoints covered:
  GET /api/manager
  GET /api/manager/<manager_id>
  PUT /api/manager/<manager_id>
"""
import pytest
from tests.conftest import auth_headers

class TestManagerResource:
    """Tests for manager profile management by Owners and Managers."""

    def test_get_all_managers_as_manager_success(self, client, manager_token):
        """TC-MGR-01: Manager can retrieve list of all managers."""
        rv = client.get('/api/manager', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert 'manager_email' in data[0]

    def test_get_single_manager_success(self, client, manager_token):
        """TC-MGR-02: Manager can retrieve a specific manager profile."""
        # First get all to find a valid ID
        all_rv = client.get('/api/manager', headers=auth_headers(manager_token))
        all_data = all_rv.get_json()
        
        if all_data:
            mgr_id = all_data[0]['manager_id']
            rv = client.get(f'/api/manager/{mgr_id}', headers=auth_headers(manager_token))
            assert rv.status_code == 200
            assert rv.get_json()['manager_id'] == mgr_id
        else:
            pytest.skip("No managers found in DB")

    def test_update_own_manager_profile_success(self, client, manager_token):
        """TC-MGR-03: Manager can update their own profile."""
        # 1. Identify current manager ID
        # Since dummy data might not expose 'id' easily, we use all_data[0] for the logged in mgr
        all_rv = client.get('/api/manager', headers=auth_headers(manager_token))
        mgr_data = all_rv.get_json()[0]
        mgr_id = mgr_data['manager_id']
        
        new_contact = "9988776655"
        rv = client.put(f'/api/manager/{mgr_id}', 
                        headers=auth_headers(manager_token),
                        json={'manager_contact': new_contact})
        assert rv.status_code == 200
        assert "Manager updated successfully" in rv.get_json()['message']
        
        # Verify via GET
        get_rv = client.get(f'/api/manager/{mgr_id}', headers=auth_headers(manager_token))
        assert get_rv.get_json()['manager_contact'] == new_contact

    def test_update_other_manager_profile_forbidden(self, client, manager_token):
        """TC-MGR-04: Manager cannot update another manager's profile."""
        # Assuming there's a second manager or we use a fake large ID
        rv = client.put('/api/manager/999', 
                        headers=auth_headers(manager_token),
                        json={'manager_name': 'Hacker'})
        assert rv.status_code == 403
        assert "Unauthorized" in rv.get_json()['message']

    def test_manager_resource_forbidden_for_staff(self, client, staff_token):
        """TC-MGR-05: Staff members are denied access to manager profiles."""
        rv = client.get('/api/manager', headers=auth_headers(staff_token))
        assert rv.status_code == 403

    def test_manager_resource_unauthenticated(self, client):
        """TC-MGR-06: No token -> 401/302."""
        rv = client.get('/api/manager')
        assert rv.status_code in (401, 302)
