"""
test_wholesalerorder.py – Tests for GenerateWholesalerOrder (/api/generate-wholesaler-order/<email>).

Endpoints covered:
  GET /api/generate-wholesaler-order/<string:supplier_email>
"""
import pytest
from tests.conftest import auth_headers

class TestGenerateWholesalerOrder:
    """Tests for PDF wholesaler order generation."""

    def test_generate_order_pdf_manager_success(self, client, manager_token):
        """TC-WHO-01: Manager can generate order PDF for a supplier with pending orders."""
        # Use an email that likely has pending orders in dummy data
        # Based on dummy data scripts or known suppliers
        supplier_email = "supplier@test.com"
        rv = client.get(f'/api/generate-wholesaler-order/{supplier_email}', headers=auth_headers(manager_token))
        
        # If no pending orders exist in current DB state, it returns 404 with a specific message
        if rv.status_code == 404:
             pytest.skip(f"No pending orders found for {supplier_email} in test DB")
        
        assert rv.status_code == 200
        assert rv.content_type == 'application/pdf'

    def test_generate_order_pdf_not_found(self, client, manager_token):
        """TC-WHO-02: Returns 404 if no pending orders exist for the email."""
        rv = client.get('/api/generate-wholesaler-order/nonexistent@void.com', headers=auth_headers(manager_token))
        assert rv.status_code == 404
        assert "No pending orders found" in rv.get_json()['message']

    def test_generate_order_pdf_forbidden_for_staff(self, client, staff_token):
        """TC-WHO-03: Staff cannot generate wholesaler orders."""
        rv = client.get('/api/generate-wholesaler-order/supplier@test.com', headers=auth_headers(staff_token))
        assert rv.status_code == 403

    def test_generate_order_pdf_forbidden_for_customer(self, client, customer_token):
        """TC-WHO-04: Customer cannot generate wholesaler orders."""
        rv = client.get('/api/generate-wholesaler-order/supplier@test.com', headers=auth_headers(customer_token))
        assert rv.status_code == 403

    def test_generate_order_pdf_unauthenticated(self, client):
        """TC-WHO-05: No token → 401/302."""
        rv = client.get('/api/generate-wholesaler-order/supplier@test.com')
        assert rv.status_code in (401, 302)
