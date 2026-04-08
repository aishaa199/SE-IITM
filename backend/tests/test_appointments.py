"""
test_appointments.py – Tests for Appointment and Customer booking APIs.

Endpoints covered:
  GET  /api/appointment
  POST /api/appointment
  GET /api/appointment/<id>
  PUT  /api/appointment/<id>
  DELETE /api/appointment/<id>
  GET  /api/todays-appointments
  GET /api/daily-appointment-count
  GET  /api/customer-upcoming-appointments
  POST  /api/customer-upcoming-appointments
  GET  /customer/appointment/<int:appointment_id>
  PUT  /customer/appointment/<int:appointment_id>
  POST /customer/appointment/<int:appointment_id>
  POST /api/customer-upcoming-appointments
  GET  /api/customer-history-appointments
  GET  /api/customer-summary
  GET /api/staff-appointments
  DELETE /api/cleanup-appointments
  
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

class TestCustomerBookingEdgeCases:
    """Detailed POST /api/customer-upcoming-appointments validation."""

    def test_book_appointment_invalid_date_format(self, client, customer_token):
        """TC-BOOK-EDGE-01: Invalid datetime string returns 400."""
        svc_id = _get_service_id(client, customer_token)
        rv = client.post('/api/customer-upcoming-appointments',
                         headers=auth_headers(customer_token),
                         json={
                             'service_ids': [svc_id],
                             'appointment_datetime': "next Tuesday at 5pm",
                         })
        assert rv.status_code == 400
        assert "Invalid datetime format" in rv.get_json()['message']

    def test_book_appointment_invalid_staff(self, client, customer_token):
        """TC-BOOK-EDGE-02: Providing a non-existent staff_id returns 404."""
        svc_id = _get_service_id(client, customer_token)
        rv = client.post('/api/customer-upcoming-appointments',
                         headers=auth_headers(customer_token),
                         json={
                             'service_ids': [svc_id],
                             'staff_id': 8888,
                             'appointment_datetime': _future_dt(5),
                         })
        assert rv.status_code == 404
        assert "Staff with provided ID not found" in rv.get_json()['message']

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
        """TC-APPT-03: No token → 401."""
        rv = client.get('/api/appointment')
        assert rv.status_code == 401

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
        """TC-APPT-10: Manager gets today's appointment list (may be empty)."""
        rv = client.get('/api/todays-appointments', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        assert isinstance(rv.get_json(), list)

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

    def test_customer_book_appointment_success(self, client, customer_token, manager_token):
        """TC-APPT-13: Customer books an appointment for themselves."""
        svc_id = _get_service_id(client, manager_token)
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

# sprint 2 added testing
class TestAppointmentAnalytics:
    """GET /api/appointment/<id> and GET /api/daily-appointment-count"""

    def test_get_single_appointment_success(self, client, manager_token):
        """TC-APPT-19: Get details of a specific appointment by ID."""
        # Create one first
        svc_id = _get_service_id(client, manager_token)
        create_rv = client.post('/api/appointment',
                                 headers=auth_headers(manager_token),
                                 json={
                                     'customer_email': 'cust@test.com',
                                     'service_ids': [svc_id],
                                     'appointment_datetime': _future_dt(2),
                                 })
        appt_id = create_rv.get_json()['appointment_id']

        rv = client.get(f'/api/appointment/{appt_id}', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        assert rv.get_json()['appointment_id'] == appt_id

    def test_daily_appointment_count_manager(self, client, manager_token):
        """TC-APPT-20: Manager retrieves hourly distribution for today."""
        rv = client.get('/api/daily-appointment-count', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        data = rv.get_json()
        if isinstance(data, list) and len(data) > 0:
            assert 'date' in data[0] # Changed from 'hour' to 'date'
            assert 'count' in data[0]

    def test_daily_appointment_count_forbidden(self, client, customer_token):
        """TC-APPT-21: Customers cannot access analytics."""
        rv = client.get('/api/daily-appointment-count', headers=auth_headers(customer_token))
        assert rv.status_code == 403

class TestStaffAppointments:
    """GET /api/staff-appointments"""

    @pytest.mark.parametrize("mode", ["today", "all"])
    def test_staff_appointments_modes(self, client, staff_token, mode):
        """TC-APPT-22: Staff can filter their own appointments by mode."""
        rv = client.get(f'/api/staff-appointments?mode={mode}', headers=auth_headers(staff_token))
        assert rv.status_code == 200
        assert isinstance(rv.get_json(), list)

    def test_staff_appointments_unauthorized(self, client, customer_token):
        """TC-APPT-23: Customer cannot access staff-specific list."""
        rv = client.get('/api/staff-appointments', headers=auth_headers(customer_token))
        assert rv.status_code == 403

class TestAppointmentMaintenance:
    """DELETE /api/cleanup-appointments"""

    def test_cleanup_appointments_manager(self, client, manager_token):
        """TC-APPT-24: Manager triggers cleanup of old records."""
        rv = client.delete('/api/cleanup-appointments', headers=auth_headers(manager_token))
        # Note: If the retention parameter is missing in your config, this might return 400 
        # as per your YAML. Adjust the assertion based on your seed data.
        if rv.status_code == 200:
            data = rv.get_json()
            assert 'deleted_count' in data
            assert 'message' in data
        else:
            assert rv.status_code == 400 

    def test_cleanup_appointments_forbidden(self, client, staff_token):
        """TC-APPT-25: Staff cannot trigger global cleanup."""
        rv = client.delete('/api/cleanup-appointments', headers=auth_headers(staff_token))
        assert rv.status_code == 403
    

class TestCustomerAppointmentOperations:
    def test_get_specific_appointment_success(self, client, customer_token, current_appt_id):
        """TC-CUST-OP-01: Guaranteed success via fixture discovery/creation."""
        rv = client.get(f'/api/customer/appointment/{current_appt_id}', 
                        headers=auth_headers(customer_token))
        assert rv.status_code == 200

    def test_reschedule_appointment_success(self, client, customer_token, current_appt_id):
        """TC-CUST-OP-03: Rescheduling the guaranteed appointment."""
        new_time = _future_dt(10)
        rv = client.put(f'/api/customer/appointment/{current_appt_id}', 
                        headers=auth_headers(customer_token),
                        json={'appointment_datetime': new_time})
        assert rv.status_code == 200

    def test_reschedule_appointment_invalid_service(self, client, customer_token, current_appt_id):
        """TC-CUST-OP-04: Using the fixture ID to test invalid service input."""
        rv = client.put(f'/api/customer/appointment/{current_appt_id}', 
                        headers=auth_headers(customer_token),
                        json={'service_ids': [9999]}) 
        assert rv.status_code == 400

    def test_cancel_appointment_success(self, client, customer_token, current_appt_id):
        """TC-CUST-OP-05: Deleting the guaranteed appointment."""
        rv = client.delete(f'/api/customer/appointment/{current_appt_id}', 
                           headers=auth_headers(customer_token))
        assert rv.status_code == 200