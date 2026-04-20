"""
test_inventory.py – Tests for Product and Inventory Transaction APIs.

Endpoints covered:
  GET    /api/product
  GET    /api/product/<id>
  POST   /api/product
  PUT    /api/product/<id>
  DELETE /api/product/<id>
  GET    /api/inventory-transaction
  POST   /api/inventory-transaction
"""
import pytest
from tests.conftest import auth_headers


def _first_product_id(client, token):
    rv = client.get('/api/product', headers=auth_headers(token))
    return rv.get_json()[0]['product_id']


class TestProductCRUD:
    """GET + POST + PUT + DELETE /api/product"""

    def test_list_products_manager(self, client, manager_token):
        """TC-INV-01: Manager can list all products with correct schema."""
        rv = client.get('/api/product', headers=auth_headers(manager_token))
        data = rv.get_json()
        assert rv.status_code == 200
        assert isinstance(data, list)
        assert len(data) >= 1
        p = data[0]
        for field in ('product_id', 'product_desc', 'product_category_name',
                      'product_price', 'product_min_qoh', 'product_curr_qoh',
                      'product_low_stock_alert'):
            assert field in p, f"Missing field: {field}"

    def test_list_products_unauthenticated(self, client):
        """TC-INV-02: No token → 401/302."""
        rv = client.get('/api/product')
        assert rv.status_code in (401, 302)

    def test_get_product_by_id(self, client, manager_token):
        """TC-INV-03: Fetching product by valid ID returns correct data."""
        pid = _first_product_id(client, manager_token)
        rv = client.get(f'/api/product/{pid}', headers=auth_headers(manager_token))
        data = rv.get_json()
        assert rv.status_code == 200
        assert data['product_id'] == pid
        assert data['product_desc'] == 'Wella Shampoo 1L'

    def test_get_product_not_found(self, client, manager_token):
        """TC-INV-04: Non-existent product ID returns 404."""
        rv = client.get('/api/product/99999', headers=auth_headers(manager_token))
        assert rv.status_code == 404

    def test_create_product_success(self, client, manager_token):
        """TC-INV-05: Manager creates a new product successfully."""
        rv = client.post('/api/product',
                         headers=auth_headers(manager_token),
                         json={
                             'product_name': 'Rica Brazilian Wax 400g',
                             'product_category': 'Skin',
                             'price': 850,
                             'minimum_stock': 6,
                             'stock_quantity': 24,
                             'supplier_name': 'Rica Professional India',
                             'supplier_contact': '+91-2265108000',
                             'supplier_email': 'orders@rica.in',
                         })
        data = rv.get_json()
        assert rv.status_code == 201
        assert 'product_id' in data
        assert data['message'] == 'Product added successfully'

    def test_create_product_customer_forbidden(self, client, customer_token):
        """TC-INV-06: Customer cannot create products – 403."""
        rv = client.post('/api/product',
                         headers=auth_headers(customer_token),
                         json={
                             'product_name': 'Test',
                             'product_category': 'Hair',
                             'price': 100,
                             'minimum_stock': 2,
                             'stock_quantity': 10,
                             'supplier_name': 'Test',
                             'supplier_contact': '000',
                             'supplier_email': 'x@x.com',
                         })
        assert rv.status_code == 403

    def test_update_product_stock(self, client, manager_token):
        """TC-INV-07: Manager increases current stock quantity."""
        pid = _first_product_id(client, manager_token)
        rv = client.put(f'/api/product/{pid}',
                        headers=auth_headers(manager_token),
                        json={'stock_quantity': 50})
        assert rv.status_code == 200
        assert 'updated' in rv.get_json()['message'].lower()

    def test_update_product_low_stock_alert_auto_cleared(self, client, manager_token):
        """TC-INV-08: Restocking a low-stock product clears the alert flag."""
        # Create product with low stock
        create_rv = client.post('/api/product',
                                headers=auth_headers(manager_token),
                                json={
                                    'product_name': 'Low Stock Product',
                                    'product_category': 'Spa',
                                    'price': 500,
                                    'minimum_stock': 10,
                                    'stock_quantity': 3,  # below minimum
                                    'supplier_name': 'Test Supplier',
                                    'supplier_contact': '+91-9000000001',
                                    'supplier_email': 'sup@test.com',
                                })
        pid = create_rv.get_json()['product_id']

        # Restock
        client.put(f'/api/product/{pid}',
                   headers=auth_headers(manager_token),
                   json={'stock_quantity': 20})

        rv = client.get(f'/api/product/{pid}', headers=auth_headers(manager_token))
        data = rv.get_json()
        assert data['product_low_stock_alert'] is False

    def test_delete_product_with_transactions_blocked(self, client, manager_token, staff_token):
        """TC-INV-09: Product with linked inventory transactions cannot be deleted."""
        pid = _first_product_id(client, manager_token)

        # Create a transaction referencing this product
        client.post('/api/inventory-transaction',
                    headers=auth_headers(staff_token),
                    json={'product_id': pid, 'quantity': 1})

        rv = client.delete(f'/api/product/{pid}',
                           headers=auth_headers(manager_token))
        data = rv.get_json()
        assert rv.status_code == 400
        assert 'inventory transactions' in data['message'].lower()

    def test_delete_product_not_found(self, client, manager_token):
        """TC-INV-10: Deleting non-existent product returns 404."""
        rv = client.delete('/api/product/99999', headers=auth_headers(manager_token))
        assert rv.status_code == 404


class TestInventoryTransactions:
    """GET + POST /api/inventory-transaction"""

    def test_list_transactions_manager(self, client, manager_token):
        """TC-INV-11: Manager can view inventory transaction list."""
        rv = client.get('/api/inventory-transaction',
                        headers=auth_headers(manager_token))
        assert rv.status_code == 200
        assert isinstance(rv.get_json(), list)

    def test_create_transaction_staff(self, client, staff_token, manager_token):
        """TC-INV-12: Staff records product usage successfully."""
        pid = _first_product_id(client, manager_token)
        rv = client.post('/api/inventory-transaction',
                         headers=auth_headers(staff_token),
                         json={'product_id': pid, 'quantity': 2})
        data = rv.get_json()
        assert rv.status_code == 201
        assert 'txn_id' in data

    def test_create_transaction_no_product(self, client, staff_token):
        """TC-INV-13: Transaction without product_id returns 400."""
        rv = client.post('/api/inventory-transaction',
                         headers=auth_headers(staff_token),
                         json={'quantity': 2})
        assert rv.status_code == 400

    def test_transaction_customer_forbidden(self, client, customer_token):
        """TC-INV-14: Customer cannot record transactions."""
        rv = client.post('/api/inventory-transaction',
                         headers=auth_headers(customer_token),
                         json={'product_id': 1, 'quantity': 1})
        assert rv.status_code == 403

    def test_list_transactions_with_date_filter(self, client, manager_token):
        """TC-INV-15: Manager filters transactions by date range."""
        rv = client.get('/api/inventory-transaction?from_date=2026-01-01&to_date=2026-12-31',
                        headers=auth_headers(manager_token))
        assert rv.status_code == 200
        assert isinstance(rv.get_json(), list)
