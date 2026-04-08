"""
test_invoice.py – Tests for Invoice API.

Endpoints covered:
  GET  /api/invoice
  GET  /api/invoice/<appointment_id>
  POST /api/invoice
  GET /appointments-for-invoice
"""
import pytest
from datetime import datetime, timedelta
from tests.conftest import auth_headers
from unittest.mock import patch

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
        """TC-INV-01: Manager can list all invoices with correct fields."""
        rv = client.get('/api/get-all-invoices', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        if len(data) > 0:
            fields = ('invoice_number', 'invoice_date', 'customer_name', 
                     'staff_name', 'invoice_amount', 'status')
            for f in fields:
                assert f in data[0], f"Missing: {f}"

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

    # sprint 2
    import pytest

# SPRINT 2: Business Logic Tests
class TestInvoiceBusinessLogic:
    """Tests for specialized invoice scenarios: VIP, Discounts, Rewards, and Bonuses."""

    def test_create_invoice_vip_discount_logic(self, client, manager_token, create_customer, setup_vip_config, get_invoice):
        """TC-INV-06: Verify VIP customer receives the salon's configured VIP discount."""
        # 1. Setup: VIP config and VIP Customer are handled by fixtures
        vip_cust = create_customer(name="VIP Test User", c_type="VIP", visits=10)

        payload = {
            'customer_id': vip_cust.customer_id,
            'staff_id': 1,
            'service_ids': "1,2",
            'invoice_amount': 200.0,  # Expected VIP Discount: 15% of 200 = 30.0
            'other_charges': 10.0,
            'appointment_id': None
        }

        # 2. Act
        rv = client.post('/api/invoice', headers=auth_headers(manager_token), json=payload)
        data = rv.get_json()
        
        # 3. Assert
        assert rv.status_code == 201
        inv = get_invoice(data['invoice_number'])
        
        # Validation: Base (200 - 30) + 10 other charges = 180.0
        assert inv.invoice_amount == 170.0
        assert inv.total_invoice_amount == 180.0

    def test_create_invoice_manual_discount_stacking(self, client, manager_token, create_customer, get_invoice):
        """TC-INV-07: Verify manual discount percentage applies to the total."""
        # Setup via fixture
        cust = create_customer(name="Discount User", visits=5)

        payload = {
            'customer_id': cust.customer_id,
            'staff_id': 1,
            'service_ids': "1",
            'invoice_amount': 100.0,
            'other_charges': 20.0,
            'discount_percentage': 10.0  # 10% off the 120.0 total
        }

        rv = client.post('/api/invoice', headers=auth_headers(manager_token), json=payload)
        data = rv.get_json()
        
        assert rv.status_code == 201
        inv = get_invoice(data['invoice_number'])
        
        # Validation: (100 + 20) * 0.9 = 108.0
        assert inv.total_invoice_amount == 108.0

    def test_create_invoice_rewards_utilization_fifo(self, client, manager_token, create_customer, get_invoice, get_customer):
        """TC-INV-08: Verify that existing reward points reduce payable amount."""
        # Setup via fixture with 50 rewards
        cust = create_customer(name="Reward User", rewards=50, visits=2)

        payload = {
            'customer_id': cust.customer_id,
            'staff_id': 1,
            'service_ids': "1",
            'invoice_amount': 150.0,
            'other_charges': 0.0
        }

        rv = client.post('/api/invoice', headers=auth_headers(manager_token), json=payload)
        data = rv.get_json()
        
        inv = get_invoice(data['invoice_number'])
        updated_cust = get_customer(cust.customer_id)
        
        # Validation: Total 150, Rewards Used 50, Payable should be 100
        assert inv.rewards_utilized == 50
        assert inv.payable_invoice_amount == 100.0
        assert updated_cust.customer_available_rewards >= 0

    def test_create_invoice_first_time_bonus_logic(self, client, manager_token, create_customer, get_invoice, get_customer):
        """TC-INV-09: Verify a brand new customer receives bonus points."""
        # Setup via fixture with 0 visits
        new_cust = create_customer(name="New Customer", visits=0)

        payload = {
            'customer_id': new_cust.customer_id,
            'staff_id': 1,
            'service_ids': "1",
            'invoice_amount': 100.0
        }

        rv = client.post('/api/invoice', headers=auth_headers(manager_token), json=payload)
        
        # Validation
        updated_cust = get_customer(new_cust.customer_id)
        assert updated_cust.number_of_visits == 1
        
        inv = get_invoice(rv.get_json()['invoice_number'])
        assert inv.rewards_earned > 0
        assert updated_cust.customer_available_rewards > 0

class TestInvoiceAppointmentLookup:
    """Test suite for the GetAppointmentIDsForInvoice resource."""

    def test_get_appointments_for_invoice_filtering(self, client, manager_token, db):
        """
        TC-INV-10: Verify only appointments with status 0 or 4 are retrieved.
        """
        from application.models import Appointment, User, Customer
        import datetime

        # 1. Setup: Ensure we have a customer to link to
        cust_user = User.query.filter_by(username='test_customer').first()
        
        # 2. Clear existing appointments to have a clean slate for this test
        db.session.query(Appointment).delete()
        
        # 3. Create three appointments with different statuses
        # Status 0: Should show up
        appt_valid_0 = Appointment(
            customer_id=cust_user.id,
            appointment_datetime=datetime.datetime.now(),
            status=0
        )
        # Status 4: Should show up
        appt_valid_4 = Appointment(
            customer_id=cust_user.id,
            appointment_datetime=datetime.datetime.now(),
            status=4
        )
        # Status 1 (e.g., Cancelled): Should NOT show up
        appt_invalid = Appointment(
            customer_id=cust_user.id,
            appointment_datetime=datetime.datetime.now(),
            status=1
        )
        
        db.session.add_all([appt_valid_0, appt_valid_4, appt_invalid])
        db.session.commit()

        # 4. Act: Call the endpoint
        rv = client.get('/api/get-appointments-for-invoice', headers=auth_headers(manager_token))
        data = rv.get_json()

        # 5. Assert
        assert rv.status_code == 200
        assert isinstance(data, list)
        
        # Check that we only got 2 results (status 0 and 4)
        assert len(data) == 2
        
        # Verify structure of the returned objects
        for item in data:
            assert "appointment_id" in item
            assert "customer_name" in item
            assert "staff_name" in item
            assert "datetime" in item
            assert item["status"] in [0, 4]
            assert item["status"] != 1