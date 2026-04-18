"""
test_services.py – Tests for Service CRUD API.

Endpoints covered:
  GET  /api/service
  GET  /api/service/<id>
  POST /api/service
  PUT  /api/service/<id>
  DELETE /api/service/<id>
"""
import pytest
from tests.conftest import auth_headers


class TestGetServices:
    """GET /api/service"""

    def test_list_services_authenticated(self, client, manager_token):
        """TC-SVC-01: Authenticated manager can list all services."""
        rv = client.get('/api/service', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1
        # Verify expected fields on first item
        first = data[0]
        for field in ('service_id', 'service_desc', 'service_category',
                      'service_price', 'service_duration'):
            assert field in first, f"Missing field: {field}"

    def test_list_services_unauthenticated(self, client):
        """TC-SVC-02: No token → 401/302."""
        rv = client.get('/api/service')
        assert rv.status_code in (401, 302)

    def test_get_single_service_success(self, client, manager_token):
        """TC-SVC-03: Fetch seeded service by ID returns correct data."""
        # Get the list first to find a valid ID
        list_rv = client.get('/api/service', headers=auth_headers(manager_token))
        service_id = list_rv.get_json()[0]['service_id']

        rv = client.get(f'/api/service/{service_id}', headers=auth_headers(manager_token))
        data = rv.get_json()
        assert rv.status_code == 200
        assert data['service_id'] == service_id
        assert data['service_desc'] == 'Ladies Haircut & Styling'
        # The seeded price is 600.0 (previously 550.0 in some versions)
        assert data['service_price'] == 600.0

    def test_get_nonexistent_service(self, client, manager_token):
        """TC-SVC-04: Fetching non-existent service ID returns 404."""
        rv = client.get('/api/service/99999', headers=auth_headers(manager_token))
        assert rv.status_code == 404

    def test_customer_can_list_services(self, client, customer_token):
        """TC-SVC-05: Customer role can also browse services."""
        rv = client.get('/api/service', headers=auth_headers(customer_token))
        assert rv.status_code == 200


class TestCreateService:
    """POST /api/service"""

    def test_create_service_success(self, client, manager_token):
        """TC-SVC-06: Manager creates a new service with all required fields."""
        rv = client.post('/api/service',
                         headers=auth_headers(manager_token),
                         json={
                             'service_desc': 'Gold Facial',
                             'service_category': 'Skin',
                             'service_price': 1400,
                             'service_duration': 75,
                             'service_products': 'Shahnaz Gold Kit',
                         })
        data = rv.get_json()
        assert rv.status_code == 201
        assert 'service_id' in data
        assert data['message'] == 'Service created successfully'

    def test_create_service_unauthorized_customer(self, client, customer_token):
        """TC-SVC-07: Customer cannot create a service – returns 403."""
        rv = client.post('/api/service',
                         headers=auth_headers(customer_token),
                         json={
                             'service_desc': 'Hack Service',
                             'service_category': 'Hair',
                             'service_price': 100,
                             'service_duration': 30,
                         })
        assert rv.status_code == 403

    def test_create_service_no_auth(self, client):
        """TC-SVC-08: No token → 401."""
        rv = client.post('/api/service',
                         json={'service_desc': 'X', 'service_category': 'Hair',
                               'service_price': 100, 'service_duration': 30})
        assert rv.status_code == 401

    def test_create_service_missing_price(self, client, manager_token):
        """TC-SVC-09 (FAILING): Missing service_price – backend should return 400 but currently
        returns 201 with NULL price because no server-side validation exists.
        Bug: ProductResource.post() does not validate required numeric fields.
        Fix: Add explicit check – if not data.get('service_price'): return 400.
        """
        rv = client.post('/api/service',
                         headers=auth_headers(manager_token),
                         json={
                             'service_desc': 'No Price Service',
                             'service_category': 'Hair',
                             # service_price intentionally omitted
                             'service_duration': 30,
                         })
        # EXPECTED: 400 Bad Request
        # ACTUAL:   201 Created (with NULL price) ← THIS IS THE BUG
        assert rv.status_code == 400, (
            "BUG DEMONSTRATED: Backend accepts a service without a price. "
            "Expected 400, got 201. Fix: validate service_price in ServiceResource.post()."
        )


class TestUpdateService:
    """PUT /api/service/<id>"""

    def _get_first_service_id(self, client, token):
        rv = client.get('/api/service', headers=auth_headers(token))
        return rv.get_json()[0]['service_id']

    def test_update_service_price(self, client, manager_token):
        """TC-SVC-10: Manager updates service price successfully."""
        sid = self._get_first_service_id(client, manager_token)
        rv = client.put(f'/api/service/{sid}',
                        headers=auth_headers(manager_token),
                        json={'service_price': 600})
        assert rv.status_code == 200
        assert 'updated' in rv.get_json()['message'].lower()

    def test_update_nonexistent_service(self, client, manager_token):
        """TC-SVC-11: Updating non-existent service returns 404."""
        rv = client.put('/api/service/99999',
                        headers=auth_headers(manager_token),
                        json={'service_price': 999})
        assert rv.status_code == 404

    def test_update_service_staff_forbidden(self, client, staff_token):
        """TC-SVC-12: Staff cannot update a service."""
        rv = client.put('/api/service/1',
                        headers=auth_headers(staff_token),
                        json={'service_price': 100})
        assert rv.status_code == 403


class TestDeleteService:
    """DELETE /api/service/<id>"""

    def test_delete_service_success(self, client, manager_token):
        """TC-SVC-13: Manager can delete a service that has no appointments."""
        # Create a throwaway service first
        create_rv = client.post('/api/service',
                                headers=auth_headers(manager_token),
                                json={
                                    'service_desc': 'Delete Me',
                                    'service_category': 'Nails',
                                    'service_price': 200,
                                    'service_duration': 20,
                                })
        sid = create_rv.get_json()['service_id']

        rv = client.delete(f'/api/service/{sid}',
                           headers=auth_headers(manager_token))
        assert rv.status_code == 200
        assert 'deleted' in rv.get_json()['message'].lower()

    def test_delete_nonexistent_service(self, client, manager_token):
        """TC-SVC-14: Deleting non-existent service returns 404."""
        rv = client.delete('/api/service/99999',
                           headers=auth_headers(manager_token))
        assert rv.status_code == 404
