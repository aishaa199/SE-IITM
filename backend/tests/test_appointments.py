"""
test_appointments.py – Tests for Appointment and Customer booking APIs.

Endpoints covered:
  GET  /api/appointment
  POST /api/appointment
  PUT  /api/appointment/<id>
  DELETE /api/appointment/<id>
  GET  /api/todays-appointments
  GET  /api/customer-upcoming-appointments
  POST /api/customer-upcoming-appointments
  GET  /api/customer-history-appointments
  GET  /api/customer-summary
"""
import pytest
from datetime import datetime, timedelta
from tests.conftest import auth_headers


def _future_dt(days=5):
    dt = datetime.now() + timedelta(days=days)
    return dt.replace(second=0, microsecond=0).isoformat()


def _get_service_id(client, token):
    rv = client.get('/api/service', headers=auth_headers(token))
    return rv.get_json()[0]['service_id']


def _get_staff_id(client, token):
    rv = client.get('/api/staff', headers=auth_headers(token))
    items = rv.get_json()
    return items[0]['staff_id'] if items else None


class TestManagerAppointments:
    """GET + POST + PUT + DELETE /api/appointment"""

    def test_list_appointments_manager(self, client, manager_token):
        """TC-APPT-01: Manager can list all appointments."""
        rv = client.get('/api/appointment', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        assert isinstance(rv.get_json(), list)

    def test_list_appointments_customer_forbidden(self, client, customer_token):
        """TC-APPT-02: Customer cannot access manager appointment list."""
        rv = client.get('/api/appointment', headers=auth_headers(customer_token))
        assert rv.status_code == 403

    def test_list_appointments_unauthenticated(self, client):
        """TC-APPT-03: No token → 401/302."""
        rv = client.get('/api/appointment')
        assert rv.status_code in (401, 302)

    def test_create_appointment_success(self, client, manager_token):
        """TC-APPT-04: Manager creates appointment with valid customer email and service."""
        svc_id = _get_service_id(client, manager_token)
        staff_id = _get_staff_id(client, manager_token)
        rv = client.post('/api/appointment',
                         headers=auth_headers(manager_token),
                         json={
                             'customer_email': 'cust@test.com',
                             'staff_id': staff_id,
                             'service_ids': [svc_id],
                             'appointment_datetime': _future_dt(3),
                         })
        data = rv.get_json()
        assert rv.status_code == 201
        assert 'appointment_id' in data

    def test_create_appointment_invalid_customer(self, client, manager_token):
        """TC-APPT-05: Creating appointment for unknown email returns 404."""
        svc_id = _get_service_id(client, manager_token)
        rv = client.post('/api/appointment',
                         headers=auth_headers(manager_token),
                         json={
                             'customer_email': 'nobody@nowhere.com',
                             'service_ids': [svc_id],
                             'appointment_datetime': _future_dt(3),
                         })
        assert rv.status_code == 404

    def test_create_appointment_no_service(self, client, manager_token):
        """TC-APPT-06: Missing service_ids returns 400."""
        rv = client.post('/api/appointment',
                         headers=auth_headers(manager_token),
                         json={
                             'customer_email': 'cust@test.com',
                             'appointment_datetime': _future_dt(3),
                         })
        assert rv.status_code == 400

    def test_update_appointment_status(self, client, manager_token):
        """TC-APPT-07: Manager can change appointment status to Completed (1)."""
        # Create appointment first
        svc_id = _get_service_id(client, manager_token)
        create_rv = client.post('/api/appointment',
                                headers=auth_headers(manager_token),
                                json={
                                    'customer_email': 'cust@test.com',
                                    'service_ids': [svc_id],
                                    'appointment_datetime': _future_dt(4),
                                })
        appt_id = create_rv.get_json()['appointment_id']

        rv = client.put(f'/api/appointment/{appt_id}',
                        headers=auth_headers(manager_token),
                        json={'status': 1})
        assert rv.status_code == 200
        assert 'updated' in rv.get_json()['message'].lower()

    def test_delete_appointment(self, client, manager_token):
        """TC-APPT-08: Manager can delete an appointment."""
        svc_id = _get_service_id(client, manager_token)
        create_rv = client.post('/api/appointment',
                                headers=auth_headers(manager_token),
                                json={
                                    'customer_email': 'cust@test.com',
                                    'service_ids': [svc_id],
                                    'appointment_datetime': _future_dt(6),
                                })
        appt_id = create_rv.get_json()['appointment_id']

        rv = client.delete(f'/api/appointment/{appt_id}',
                           headers=auth_headers(manager_token))
        assert rv.status_code == 200

    def test_delete_nonexistent_appointment(self, client, manager_token):
        """TC-APPT-09: Deleting non-existent appointment returns 404."""
        rv = client.delete('/api/appointment/99999',
                           headers=auth_headers(manager_token))
        assert rv.status_code == 404


class TestTodaysAppointments:
    """GET /api/todays-appointments"""

    def test_todays_appointments_manager(self, client, manager_token):
        """TC-APPT-10: Manager gets today's appointment list (list or empty-message dict)."""
        rv = client.get('/api/todays-appointments', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        # Backend returns [] list OR {"message": "No appointments found..."} when empty
        body = rv.get_json()
        assert isinstance(body, (list, dict))

    def test_todays_appointments_staff(self, client, staff_token):
        """TC-APPT-11: Staff member can also fetch today's appointments."""
        rv = client.get('/api/todays-appointments', headers=auth_headers(staff_token))
        assert rv.status_code == 200

    def test_todays_appointments_customer_forbidden(self, client, customer_token):
        """TC-APPT-12: Customer cannot access today's appointments endpoint."""
        rv = client.get('/api/todays-appointments', headers=auth_headers(customer_token))
        assert rv.status_code == 403


class TestCustomerSelfBooking:
    """POST /api/customer-upcoming-appointments (customer self-booking)"""

    def test_customer_book_appointment_success(self, client, customer_token):
        """TC-APPT-13: Customer books an appointment (uses customer_token for service lookup too)."""
        svc_id = _get_service_id(client, customer_token)
        rv = client.post('/api/customer-upcoming-appointments',
                         headers=auth_headers(customer_token),
                         json={
                             'service_ids': [svc_id],
                             'appointment_datetime': _future_dt(7),
                         })
        data = rv.get_json()
        assert rv.status_code == 201
        assert 'appointment_id' in data

    def test_customer_book_no_service(self, client, customer_token):
        """TC-APPT-14: Customer booking without service IDs returns 400."""
        rv = client.post('/api/customer-upcoming-appointments',
                         headers=auth_headers(customer_token),
                         json={
                             'appointment_datetime': _future_dt(7),
                         })
        assert rv.status_code == 400

    def test_customer_get_upcoming(self, client, customer_token):
        """TC-APPT-15: Customer retrieves their upcoming appointments."""
        rv = client.get('/api/customer-upcoming-appointments',
                        headers=auth_headers(customer_token))
        assert rv.status_code == 200
        assert isinstance(rv.get_json(), list)

    def test_customer_get_history(self, client, customer_token):
        """TC-APPT-16: Customer retrieves appointment history."""
        rv = client.get('/api/customer-history-appointments',
                        headers=auth_headers(customer_token))
        assert rv.status_code == 200
        assert isinstance(rv.get_json(), list)


class TestCustomerSummary:
    """GET /api/customer-summary"""

    def test_customer_summary_success(self, client, customer_token):
        """TC-APPT-17: Customer summary returns expected fields."""
        rv = client.get('/api/customer-summary', headers=auth_headers(customer_token))
        data = rv.get_json()
        assert rv.status_code == 200
        for field in ('customer_type', 'upcoming_appointments_count',
                      'past_appointments_count', 'available_rewards'):
            assert field in data, f"Missing field: {field}"

    def test_customer_summary_manager_forbidden(self, client, manager_token):
        """TC-APPT-18: Manager cannot call customer-summary endpoint."""
        rv = client.get('/api/customer-summary', headers=auth_headers(manager_token))
        assert rv.status_code == 403
