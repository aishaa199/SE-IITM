"""
test_invoiceappointments.py – Tests for GetAppointmentIDsForInvoice (/api/get-appointments-for-invoice).

Endpoints covered:
  GET /api/get-appointments-for-invoice
"""
import pytest
from tests.conftest import auth_headers

class TestGetAppointmentIDsForInvoice:
    """Tests for searching appointments eligible for invoicing (status 0 or 4)."""

    def test_get_appointments_for_invoice_manager_success(self, client, manager_token):
        """TC-INV-APP-01: Manager can retrieve appointments with status 0 or 4."""
        rv = client.get('/api/get-appointments-for-invoice', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        for appt in data:
            assert 'appointment_id' in appt
            assert appt['status'] in [0, 4]

    def test_get_appointments_for_invoice_staff_success(self, client, staff_token):
        """TC-INV-APP-02: Staff can retrieve appointments with status 0 or 4."""
        rv = client.get('/api/get-appointments-for-invoice', headers=auth_headers(staff_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)

    def test_get_appointments_for_invoice_forbidden_for_customer(self, client, customer_token):
        """TC-INV-APP-03: Customer cannot access this endpoint."""
        rv = client.get('/api/get-appointments-for-invoice', headers=auth_headers(customer_token))
        assert rv.status_code == 403

    def test_get_appointments_for_invoice_unauthenticated(self, client):
        """TC-INV-APP-04: No token → 401/302."""
        rv = client.get('/api/get-appointments-for-invoice')
        assert rv.status_code in (401, 302)
