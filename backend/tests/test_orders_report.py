"""
test_orders_report.py – Tests for SupplierOrderReportResource.

Endpoints covered:
  GET /api/supplier-order-reports
"""
import pytest
from tests.conftest import auth_headers

class TestSupplierOrderReport:
    """Manager-facing supplier order report generation."""

    def test_get_supplier_report_no_orders(self, client, manager_token):
        """TC-ORD-RPT-01: Returns 404 if no pending orders exist."""
        rv = client.get('/api/supplier-order-reports', headers=auth_headers(manager_token))
        # If the test is returning 200/404 based on the actual DB state, 
        # let's be precise about what we expect from the RESOURCE code.
        assert rv.status_code == 404
        data = rv.get_json()
        assert "No pending orders found" in data.get('message', '')

    def test_get_supplier_report_success(self, client, manager_token, db, app):
        """TC-ORD-RPT-02: Successfully generates reports when pending orders exist."""
        from application.models import Order, Product
        with app.app_context():
            product = Product.query.first()
            # Create a pending order with required fields
            order = Order(
                product_id=product.product_id,
                order_quantity=10,
                supplier_name="Test Supplier",
                supplier_email="supplier@test.com",
                status=0 # Pending
            )
            db.session.add(order)
            db.session.commit()

        rv = client.get('/api/supplier-order-reports', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert "Successfully generated" in data.get('message', '')

    def test_get_supplier_report_forbidden(self, client, staff_token):
        """TC-ORD-RPT-03: Staff/Customer access is forbidden."""
        rv = client.get('/api/supplier-order-reports', headers=auth_headers(staff_token))
        assert rv.status_code == 403

    def test_get_supplier_report_unauthenticated(self, client):
        """TC-ORD-RPT-04: Unauthenticated access is denied."""
        rv = client.get('/api/supplier-order-reports')
        assert rv.status_code in (401, 302)
