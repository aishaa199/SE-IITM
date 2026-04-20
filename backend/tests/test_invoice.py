"""
test_invoice.py – Tests for Invoice API.

Endpoints covered:
  GET  /api/invoice
  GET  /api/invoice/<appointment_id>
  POST /api/invoice
"""
import pytest
from datetime import datetime, timedelta
from tests.conftest import auth_headers

def _get_service_id(client, token):
    rv = client.get('/api/service', headers=auth_headers(token))
    data = rv.get_json()
    return data[0]['service_id'] if data else None

def _get_staff_id(client, token):
    rv = client.get('/api/staff', headers=auth_headers(token))
    data = rv.get_json()
    return data[0]['staff_id'] if data else None

def _create_appointment(client, manager_token, customer_email='cust@test.com'):
    svc_id = _get_service_id(client, manager_token)
    staff_id = _get_staff_id(client, manager_token)
    dt = (datetime.now() + timedelta(days=1)).replace(second=0, microsecond=0).isoformat()
    rv = client.post('/api/appointment',
                     headers=auth_headers(manager_token),
                     json={
                         'customer_email': customer_email,
                         'staff_id': staff_id,
                         'service_ids': [svc_id],
                         'appointment_datetime': dt,
                     })
    return rv.get_json().get('appointment_id')


class TestInvoiceAPI:
    """Tests for manager/staff invoice operations."""

    def test_list_invoices_manager(self, client, manager_token):
        """TC-INV-01: GET /api/invoice without ID returns uninvoiced appointments list."""
        rv = client.get('/api/invoice', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        # Each item is an appointment awaiting invoicing
        if len(data) > 0:
            assert 'appointment_id' in data[0]

    def test_list_invoices_unauthenticated(self, client):
        """TC-INV-02: No token → 302/401 (depends on setup)."""
        rv = client.get('/api/invoice')
        assert rv.status_code in (302, 401)

    def test_list_invoices_customer_forbidden(self, client, customer_token):
        """TC-INV-03: Customer role cannot access invoice list."""
        rv = client.get('/api/invoice', headers=auth_headers(customer_token))
        assert rv.status_code == 403

    def test_get_invoice_data_for_appointment(self, client, manager_token):
        """TC-INV-04: Manager fetches data required to create an invoice for an appointment."""
        appt_id = _create_appointment(client, manager_token)
        rv = client.get(f'/api/invoice/{appt_id}', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert 'customer_id' in data
        assert 'service_total' in data
        assert 'service_ids' in data

    def test_create_invoice_success(self, client, manager_token):
        """TC-INV-05: Manager creates an invoice successfully."""
        appt_id = _create_appointment(client, manager_token)
        # First get the data needed for invoice
        data_rv = client.get(f'/api/invoice/{appt_id}', headers=auth_headers(manager_token))
        prep = data_rv.get_json()
        
        rv = client.post('/api/invoice',
                         headers=auth_headers(manager_token),
                         json={
                             'customer_id': prep['customer_id'],
                             'staff_id': prep['staff_id'],
                             'service_ids': prep['service_ids'],
                             'invoice_amount': prep['service_total'],
                             'appointment_id': appt_id,
                             'other_charges': 10.0
                         })
        data = rv.get_json()
        assert rv.status_code == 201
        assert 'invoice_number' in data

    def test_create_invoice_missing_fields(self, client, manager_token):
        """TC-INV-06: Missing required fields (customer_id) returns 400."""
        rv = client.post('/api/invoice',
                         headers=auth_headers(manager_token),
                         json={
                             'staff_id': 1,
                             'service_ids': '1',
                             'invoice_amount': 100
                         })
        assert rv.status_code == 400

    def test_get_existing_invoice_by_appointment(self, client, manager_token):
        """TC-INV-07: Fetching an existing invoice by appointment_id returns full record."""
        appt_id = _create_appointment(client, manager_token)
        data_rv = client.get(f'/api/invoice/{appt_id}', headers=auth_headers(manager_token))
        prep = data_rv.get_json()
        
        client.post('/api/invoice',
                    headers=auth_headers(manager_token),
                    json={
                        'customer_id': prep['customer_id'],
                        'staff_id': prep['staff_id'],
                        'service_ids': prep['service_ids'],
                        'invoice_amount': prep['service_total'],
                        'appointment_id': appt_id
                    })
        
        rv = client.get(f'/api/invoice/{appt_id}', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert 'invoice_number' in data
        assert 'service_descs' in data

    def test_create_invoice_invalid_customer(self, client, manager_token):
        """TC-INV-08: Creating invoice for non-existent customer returns 404."""
        rv = client.post('/api/invoice',
                         headers=auth_headers(manager_token),
                         json={
                             'customer_id': 99999,
                             'staff_id': 1,
                             'service_ids': '1',
                             'invoice_amount': 100
                         })
        assert rv.status_code == 404

    def test_get_invoice_appointment_not_found(self, client, manager_token):
        """TC-INV-09: Fetching invoice data for non-existent appointment returns 404."""
        rv = client.get('/api/invoice/99999', headers=auth_headers(manager_token))
        assert rv.status_code == 404
