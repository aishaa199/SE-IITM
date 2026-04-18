"""
test_staffappointments.py - Tests for StaffAppointmentResource.

Endpoints covered:
  GET /api/staff-appointments
"""
import pytest
from datetime import datetime, timedelta
from tests.conftest import auth_headers

def _get_future_dt(days=0):
    dt = datetime.now() + timedelta(days=days)
    return dt.replace(second=0, microsecond=0)

@pytest.fixture
def staff_appointment_setup(client, manager_token, db, app):
    """Setup an appointment for the test staff."""
    from application.models import Staff, Customer, Service, Appointment
    with app.app_context():
        staff = Staff.query.filter_by(staff_email='staff@test.com').first()
        customer = Customer.query.filter_by(customer_email='cust@test.com').first()
        service = Service.query.first()
        
        # Create a 'today' appointment
        appt_today = Appointment(
            customer_id=customer.customer_id,
            staff_id=staff.staff_id,
            appointment_datetime=_get_future_dt(0),
            status=0 # Pending
        )
        appt_today.services.append(service)
        
        # Create a 'past/future' appointment (not today)
        appt_future = Appointment(
            customer_id=customer.customer_id,
            staff_id=staff.staff_id,
            appointment_datetime=_get_future_dt(2),
            status=0
        )
        appt_future.services.append(service)
        
        db.session.add(appt_today)
        db.session.add(appt_future)
        db.session.commit()
        
        return {
            'staff_id': staff.staff_id,
            'appt_today_id': appt_today.appointment_id,
            'appt_future_id': appt_future.appointment_id
        }

class TestStaffAppointments:
    """GET /api/staff-appointments"""

    def test_get_staff_appointments_today_success(self, client, staff_token, staff_appointment_setup):
        """TC-STF-APPT-01: Staff can get their appointments for today."""
        rv = client.get('/api/staff-appointments', headers=auth_headers(staff_token), query_string={'mode': 'today'})
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1
        # Check if the returned appointment is the one for today
        found = any(item['appointment_id'] == staff_appointment_setup['appt_today_id'] for item in data)
        assert found is True

    def test_get_staff_appointments_all_success(self, client, staff_token, staff_appointment_setup):
        """TC-STF-APPT-02: Staff can get all their appointments."""
        rv = client.get('/api/staff-appointments', headers=auth_headers(staff_token), query_string={'mode': 'all'})
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        assert len(data) >= 2
        
        ids = [item['appointment_id'] for item in data]
        assert staff_appointment_setup['appt_today_id'] in ids
        assert staff_appointment_setup['appt_future_id'] in ids

    def test_get_staff_appointments_default_mode(self, client, staff_token, staff_appointment_setup):
        """TC-STF-APPT-03: Default mode is 'today'."""
        rv = client.get('/api/staff-appointments', headers=auth_headers(staff_token))
        assert rv.status_code == 200
        data = rv.get_json()
        # Should be same as 'today'
        ids = [item['appointment_id'] for item in data]
        assert staff_appointment_setup['appt_today_id'] in ids
        # Future appointment should NOT be in 'today' results usually, unless it is actually today's date
        assert staff_appointment_setup['appt_future_id'] not in ids

    def test_get_staff_appointments_invalid_mode(self, client, staff_token):
        """TC-STF-APPT-04: Invalid mode returns 400."""
        rv = client.get('/api/staff-appointments', headers=auth_headers(staff_token), query_string={'mode': 'invalid'})
        assert rv.status_code == 400
        assert rv.get_json()['message'] == "Invalid mode. Use 'today' or 'all'."

    def test_get_staff_appointments_forbidden_for_customer(self, client, customer_token):
        """TC-STF-APPT-05: Customer cannot access staff appointments."""
        # Use a fresh client to avoid session leakage from previous tests
        from main import create_app
        fresh_client = create_app().test_client()
        rv = fresh_client.get('/api/staff-appointments', headers=auth_headers(customer_token))
        assert rv.status_code == 403

    def test_get_staff_appointments_unauthenticated(self, client):
        """TC-STF-APPT-06: Unauthenticated access returns 302 or 401."""
        # Use a fresh client to avoid session leakage from previous tests
        from main import create_app
        fresh_client = create_app().test_client()
        rv = fresh_client.get('/api/staff-appointments')
        assert rv.status_code in (302, 401)
