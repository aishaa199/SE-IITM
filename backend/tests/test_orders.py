"""
test_orders.py – Tests for Order management.

Endpoints:
  POST   /api/order
  GET    /api/order
  GET    /api/order/<order_id>
  PUT    /api/order/<order_id>
  DELETE /api/order/<order_id>
"""
import pytest
from tests.conftest import auth_headers

class TestOrderAPI:
    """Standardized Order API Tests."""

    def test_create_order_manager(self, client, manager_token):
        """TC-ORD-01: Manager can create a replenishment order."""
        # Need a product ID to order. Product 1 exists in seed data.
        payload = {
            "product_id": 1,
            "order_quantity": 10,
            "reason_for_order": "Low stock"
        }
        rv = client.post('/api/order', json=payload, headers=auth_headers(manager_token))
        assert rv.status_code == 201
        data = rv.get_json()
        assert data['message'] == "Replenishment order created successfully"
        
        # Verify fields in the 'order' object
        order = data['order']
        fields = ('order_id', 'product_id', 'order_quantity', 'order_cost', 'status')
        for f in fields:
            assert f in order, f"Missing field: {f}"
        
        assert order['order_quantity'] == 10
        # Backend creates orders with status=2 (default) per Order model definition
        assert 'status' in order

    def test_create_order_invalid_data(self, client, manager_token):
        """TC-ORD-02: Creating order with missing data returns 400."""
        payload = {"product_id": 1} # Missing order_quantity
        rv = client.post('/api/order', json=payload, headers=auth_headers(manager_token))
        assert rv.status_code == 400

    def test_create_order_product_not_found(self, client, manager_token):
        """TC-ORD-03: Creating order for non-existent product returns 404."""
        payload = {
            "product_id": 9999,
            "order_quantity": 5
        }
        rv = client.post('/api/order', json=payload, headers=auth_headers(manager_token))
        assert rv.status_code == 404

    def test_list_orders_manager(self, client, manager_token):
        """TC-ORD-04: Manager can list all orders."""
        rv = client.get('/api/order', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)

    def test_get_single_order_manager(self, client, manager_token):
        """TC-ORD-05: Manager can get specific order details."""
        # Create an order first
        payload = {"product_id": 1, "order_quantity": 5}
        create_rv = client.post('/api/order', json=payload, headers=auth_headers(manager_token))
        order_id = create_rv.get_json()['order']['order_id']

        rv = client.get(f'/api/order/{order_id}', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        assert rv.get_json()['order_id'] == order_id

    def test_update_order_status_processed(self, client, manager_token):
        """TC-ORD-06: Manager can mark order as Processed (1)."""
        # Create order
        payload = {"product_id": 1, "order_quantity": 10}
        create_rv = client.post('/api/order', json=payload, headers=auth_headers(manager_token))
        order_id = create_rv.get_json()['order']['order_id']

        # Update to Processed (1)
        update_payload = {"status": 1}
        rv = client.put(f'/api/order/{order_id}', json=update_payload, headers=auth_headers(manager_token))
        assert rv.status_code == 200
        assert rv.get_json()['order']['status'] == 1
        assert rv.get_json()['order']['order_replenishment_date'] is not None

    def test_update_order_invalid_date(self, client, manager_token):
        """TC-ORD-07: Updating order with invalid date format returns 400."""
        payload = {"product_id": 1, "order_quantity": 5}
        create_rv = client.post('/api/order', json=payload, headers=auth_headers(manager_token))
        order_id = create_rv.get_json()['order']['order_id']

        update_payload = {"order_replenishment_date": "invalid-date"}
        rv = client.put(f'/api/order/{order_id}', json=update_payload, headers=auth_headers(manager_token))
        assert rv.status_code == 400

    def test_delete_order_manager(self, client, manager_token):
        """TC-ORD-08: Manager can delete an order."""
        payload = {"product_id": 1, "order_quantity": 5}
        create_rv = client.post('/api/order', json=payload, headers=auth_headers(manager_token))
        order_id = create_rv.get_json()['order']['order_id']

        rv = client.delete(f'/api/order/{order_id}', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        
        # Confirm it's gone
        get_rv = client.get(f'/api/order/{order_id}', headers=auth_headers(manager_token))
        assert get_rv.status_code == 404

    def test_order_forbidden_for_staff(self, client, staff_token):
        """TC-ORD-09: Staff cannot access order endpoints."""
        rv = client.get('/api/order', headers=auth_headers(staff_token))
        assert rv.status_code == 403

    def test_order_unauthenticated(self, client):
        """TC-ORD-10: No token → 302/401."""
        rv = client.get('/api/order')
        assert rv.status_code in (302, 401)
