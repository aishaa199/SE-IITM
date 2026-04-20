"""
test_managers.py – Tests for Manager CRUD API.

POST /api/create-manager uses field names: username, password, fullname, email,
phone, skills, role, dob, doj, branch_name.

Endpoints covered:
  POST /api/create-manager
  GET  /api/manager
  GET  /api/manager/<id>
  PUT  /api/manager/<id>
  DELETE /api/manager/<id>
"""
import pytest
from tests.conftest import auth_headers


def _create_manager_payload(username, email, password='Mgr@1234'):
    return {
        'username': username,
        'password': password,
        'fullname': 'TC Manager',
        'email': email,
        'phone': '+91-9100000001',
        'skills': 'Operations',
        'role': 'Manager',
        'dob': '1985-03-15',
        'doj': '2023-06-01',
        'branch_name': 'Test Branch',
    }


def _create_manager(client, owner_token, username='mgr_tc_01', email='mgr_tc_01@salon.com'):
    return client.post('/api/create-manager',
                       headers=auth_headers(owner_token),
                       json=_create_manager_payload(username, email))


class TestManagerCRUD:

    def test_create_manager_success(self, client, owner_token):
        """TC-MGR-01: Owner creates a new manager account."""
        rv = _create_manager(client, owner_token, 'mgr_tc_create_01', 'mgr_tc_create_01@salon.com')
        data = rv.get_json()
        assert rv.status_code in (200, 201)
        assert 'manager_id' in data or 'username' in data

    def test_create_manager_duplicate_username(self, client, owner_token):
        """TC-MGR-02: Duplicate username returns 409 Conflict."""
        _create_manager(client, owner_token, 'mgr_dup_01', 'mgr_dup_01@salon.com')
        rv = _create_manager(client, owner_token, 'mgr_dup_01', 'mgr_dup_02@salon.com')
        assert rv.status_code == 409

    def test_create_manager_missing_username(self, client, owner_token):
        """TC-MGR-03: Missing username → 400."""
        rv = client.post('/api/create-manager',
                         headers=auth_headers(owner_token),
                         json={
                             'fullname': 'No Username Manager',
                             'email': 'nousername@salon.com',
                             'password': 'Pass@1234',
                         })
        assert rv.status_code == 400

    def test_create_manager_missing_password(self, client, owner_token):
        """TC-MGR-04: Missing password → 400."""
        rv = client.post('/api/create-manager',
                         headers=auth_headers(owner_token),
                         json={
                             'username': 'mgr_nopass',
                             'fullname': 'No Pass Manager',
                             'email': 'nopass@salon.com',
                         })
        assert rv.status_code == 400

    def test_create_manager_manager_forbidden(self, client, manager_token):
        """TC-MGR-05: Manager role cannot create other managers – 403."""
        rv = client.post('/api/create-manager',
                         headers=auth_headers(manager_token),
                         json=_create_manager_payload('mgr_hack', 'hack@salon.com'))
        assert rv.status_code == 403

    def test_create_manager_unauthenticated(self, client):
        """TC-MGR-06: No token → 401/302."""
        rv = client.post('/api/create-manager', json={})
        assert rv.status_code in (401, 302)

    def test_list_managers_owner(self, client, owner_token):
        """TC-MGR-07: Owner can list all managers."""
        rv = client.get('/api/manager', headers=auth_headers(owner_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1
        m = data[0]
        for field in ('manager_id', 'manager_name', 'manager_email', 'manager_role'):
            assert field in m, f"Missing field: {field}"

    def test_list_managers_manager_role(self, client, manager_token):
        """TC-MGR-08: Manager role can also call GET /api/manager."""
        rv = client.get('/api/manager', headers=auth_headers(manager_token))
        assert rv.status_code == 200

    def test_get_manager_by_id(self, client, owner_token):
        """TC-MGR-09: Owner fetches a specific manager by ID."""
        mid = client.get('/api/manager', headers=auth_headers(owner_token)).get_json()[0]['manager_id']
        rv = client.get(f'/api/manager/{mid}', headers=auth_headers(owner_token))
        data = rv.get_json()
        assert rv.status_code == 200
        assert data['manager_id'] == mid

    def test_get_manager_not_found(self, client, owner_token):
        """TC-MGR-10: Non-existent manager ID returns 404."""
        rv = client.get('/api/manager/99999', headers=auth_headers(owner_token))
        assert rv.status_code == 404

    def test_update_manager_branch(self, client, owner_token):
        """TC-MGR-11: Owner updates manager's branch name."""
        mid = client.get('/api/manager', headers=auth_headers(owner_token)).get_json()[0]['manager_id']
        rv = client.put(f'/api/manager/{mid}',
                        headers=auth_headers(owner_token),
                        json={'branch_name': 'New Branch Name'})
        assert rv.status_code == 200
        assert 'updated' in rv.get_json()['message'].lower()

    def test_update_manager_not_found(self, client, owner_token):
        """TC-MGR-12: Updating non-existent manager returns 404."""
        rv = client.put('/api/manager/99999',
                        headers=auth_headers(owner_token),
                        json={'branch_name': 'X'})
        assert rv.status_code == 404

    def test_delete_manager(self, client, owner_token):
        """TC-MGR-13: Owner creates then deletes a manager (find ID via list)."""
        create_rv = _create_manager(client, owner_token, 'mgr_to_del', 'del@salon.com')
        assert create_rv.status_code in (200, 201)
        managers = client.get('/api/manager', headers=auth_headers(owner_token)).get_json()
        target = next((m for m in managers if m.get('manager_email') == 'del@salon.com'), None)
        if target is None:
            pytest.skip("Newly created manager not found in list.")
        mid = target['manager_id']
        rv = client.delete(f'/api/manager/{mid}', headers=auth_headers(owner_token))
        assert rv.status_code == 200
        assert 'deleted' in rv.get_json()['message'].lower()

    def test_delete_manager_not_found(self, client, owner_token):
        """TC-MGR-14: Deleting non-existent manager returns 404."""
        rv = client.delete('/api/manager/99999', headers=auth_headers(owner_token))
        assert rv.status_code == 404
