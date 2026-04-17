"""
test_allinvoices.py – Tests for GetAllInvoices (/api/get-all-invoices).

Endpoints covered:
  GET /api/get-all-invoices
"""
import pytest
from tests.conftest import auth_headers

class TestGetAllInvoices:
    """Tests for manager and staff to view all invoices."""

    def test_get_all_invoices_manager_success(self, client, manager_token):
        """TC-INV-ALL-01: Manager can retrieve all invoices."""
        rv = client.get('/api/get-all-invoices', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert 'invoice_number' in data[0]
            assert 'customer_name' in data[0]

    def test_get_all_invoices_staff_success(self, client, staff_token):
        """TC-INV-ALL-02: Staff can retrieve all invoices."""
        rv = client.get('/api/get-all-invoices', headers=auth_headers(staff_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)

    def test_get_all_invoices_forbidden_for_customer(self, client, customer_token):
        """TC-INV-ALL-03: Customer cannot access list of all invoices."""
        rv = client.get('/api/get-all-invoices', headers=auth_headers(customer_token))
        assert rv.status_code == 403

    def test_get_all_invoices_unauthenticated(self, client):
        """TC-INV-ALL-04: No token → 401/302."""
        rv = client.get('/api/get-all-invoices')
        assert rv.status_code in (401, 302)
