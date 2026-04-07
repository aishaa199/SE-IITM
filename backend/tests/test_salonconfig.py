"""
test_salonconfig.py – Tests for Salon Configuration management.

Endpoints:
  GET    /api/salon-config
  GET    /api/salon-config/<setting_id>
  PUT    /api/salon-config/<setting_id>
"""
import pytest
from tests.conftest import auth_headers

class TestSalonConfigAPI:
    """Standardized SalonConfig API Tests."""

    def test_list_configs_manager(self, client, manager_token):
        """TC-CFG-01: Manager can list all salon configurations."""
        rv = client.get('/api/salon-config', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        
        # Verify fields if at least one config exists
        if len(data) > 0:
            fields = ('setting_id', 'param_name', 'param_value', 'from_date', 'to_date')
            for f in fields:
                assert f in data[0], f"Missing field: {f}"

    def test_get_single_config_manager(self, client, manager_token):
        """TC-CFG-02: Manager can get a specific configuration by ID."""
        # First list to get an ID
        list_rv = client.get('/api/salon-config', headers=auth_headers(manager_token))
        configs = list_rv.get_json()
        if not configs:
            pytest.skip("No salon configurations found to test GET single")
            
        setting_id = configs[0]['setting_id']
        rv = client.get(f'/api/salon-config/{setting_id}', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        assert rv.get_json()['setting_id'] == setting_id

    def test_get_config_not_found(self, client, manager_token):
        """TC-CFG-03: Getting non-existent config returns 404."""
        rv = client.get('/api/salon-config/9999', headers=auth_headers(manager_token))
        assert rv.status_code == 404

    def test_update_config_manager(self, client, manager_token):
        """TC-CFG-04: Manager can update a configuration parameter."""
        # First list to get an ID
        list_rv = client.get('/api/salon-config', headers=auth_headers(manager_token))
        configs = list_rv.get_json()
        if not configs:
            pytest.skip("No salon configurations found to test PUT")
            
        setting_id = configs[0]['setting_id']
        original_value = configs[0]['param_value']
        new_value = "UpdatedValue_" + original_value if original_value else "NewValue"
        
        payload = {
            "param_value": new_value,
            "from_date": "2026-01-01"
        }
        
        rv = client.put(f'/api/salon-config/{setting_id}', json=payload, headers=auth_headers(manager_token))
        assert rv.status_code == 200
        assert rv.get_json()['message'] == "Configuration updated successfully"
        
        # Verify update
        get_rv = client.get(f'/api/salon-config/{setting_id}', headers=auth_headers(manager_token))
        assert get_rv.get_json()['param_value'] == new_value

    def test_update_config_not_found(self, client, manager_token):
        """TC-CFG-05: Updating non-existent config returns 404."""
        rv = client.put('/api/salon-config/9999', json={"param_value": "test"}, headers=auth_headers(manager_token))
        assert rv.status_code == 404

    def test_list_configs_forbidden_for_staff(self, client, staff_token):
        """TC-CFG-06: Staff cannot access salon config endpoints."""
        rv = client.get('/api/salon-config', headers=auth_headers(staff_token))
        assert rv.status_code == 403

    def test_salon_config_unauthenticated(self, client):
        """TC-CFG-07: No token → 302/401."""
        rv = client.get('/api/salon-config')
        assert rv.status_code in (302, 401)
