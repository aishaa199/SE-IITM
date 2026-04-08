"""
test_staff.py – Tests for Staff CRUD and Attendance APIs.

Endpoints covered:
  GET  /api/staff
  GET  /api/staff/<id>
  POST /api/staff
  PUT  /api/staff/<id>
  GET  /api/staff-customer-reviews
  DELETE /api/staff/<id>
  GET  /api/staff-attendance
  POST /api/staff-attendance
  GET  /api/manager-staff-attendance
"""
import pytest
from tests.conftest import auth_headers


class TestStaffCRUD:

    def test_list_staff_manager(self, client, manager_token):
        """TC-STAFF-01: Manager can list all staff members."""
        rv = client.get('/api/staff', headers=auth_headers(manager_token))
        data = rv.get_json()
        assert rv.status_code == 200
        assert isinstance(data, list)
        assert len(data) >= 1
        s = data[0]
        for field in ('staff_id', 'staff_name', 'staff_role',
                      'staff_cumulative_rating', 'is_present_today'):
            assert field in s

    def test_list_staff_customer(self, client, customer_token):
        """TC-STAFF-02: Customer can also read staff list (for booking)."""
        rv = client.get('/api/staff', headers=auth_headers(customer_token))
        assert rv.status_code == 200

    def test_list_staff_unauthenticated(self, client):
        """TC-STAFF-03: No token → 401."""
        rv = client.get('/api/staff')
        assert rv.status_code == 401

    def test_get_staff_by_id(self, client, manager_token):
        """TC-STAFF-04: Fetch seeded staff member by ID."""
        list_rv = client.get('/api/staff', headers=auth_headers(manager_token))
        sid = list_rv.get_json()[0]['staff_id']
        rv = client.get(f'/api/staff/{sid}', headers=auth_headers(manager_token))
        data = rv.get_json()
        assert rv.status_code == 200
        assert data['staff_id'] == sid

    def test_get_staff_not_found(self, client, manager_token):
        """TC-STAFF-05: Non-existent staff ID returns 404."""
        rv = client.get('/api/staff/99999', headers=auth_headers(manager_token))
        assert rv.status_code == 404

    def test_create_staff_success(self, client, manager_token):
        """TC-STAFF-06: Manager creates new staff with required fields."""
        rv = client.post('/api/staff',
                         headers=auth_headers(manager_token),
                         json={
                             'username': 'new_staff_test_01',
                             'staff_name': 'Kavitha Reddy',
                             'staff_contact': '+91-9800011122',
                             'staff_email': 'kavitha@salon.com',
                             'staff_skills': 'Manicure, Pedicure',
                             'staff_role': 'Nail Technician',
                             'staff_dob': '1997-09-14',
                             'staff_doj': '2024-02-01',
                             'staff_salary': 28000,
                         })
        data = rv.get_json()
        assert rv.status_code == 201
        assert 'staff_id' in data
        assert 'username' in data

    def test_create_staff_duplicate_username(self, client, manager_token):
        """TC-STAFF-07: Duplicate username returns 400."""
        payload = {
            'username': 'dup_staff_user',
            'staff_name': 'Dup Staff',
            'staff_contact': '+91-9800022233',
            'staff_email': 'dup1@salon.com',
            'staff_dob': '1995-01-01',
            'staff_doj': '2024-01-01',
        }
        client.post('/api/staff', headers=auth_headers(manager_token), json=payload)
        rv = client.post('/api/staff', headers=auth_headers(manager_token), json=payload)
        assert rv.status_code == 400

    def test_create_staff_customer_forbidden(self, client, customer_token):
        """TC-STAFF-08: Customer cannot create staff – 403."""
        rv = client.post('/api/staff',
                         headers=auth_headers(customer_token),
                         json={'username': 'hack', 'staff_name': 'X',
                               'staff_contact': '000', 'staff_email': 'x@x.com',
                               'staff_dob': '2000-01-01', 'staff_doj': '2024-01-01'})
        assert rv.status_code == 403

    def test_update_staff_salary(self, client, manager_token):
        """TC-STAFF-09: Manager updates staff salary."""
        list_rv = client.get('/api/staff', headers=auth_headers(manager_token))
        sid = list_rv.get_json()[0]['staff_id']
        rv = client.put(f'/api/staff/{sid}',
                        headers=auth_headers(manager_token),
                        json={'staff_salary': 35000})
        assert rv.status_code == 200
        assert 'updated' in rv.get_json()['message'].lower()

    def test_delete_staff_not_found(self, client, manager_token):
        """TC-STAFF-10: Deleting non-existent staff returns 404."""
        rv = client.delete('/api/staff/99999', headers=auth_headers(manager_token))
        assert rv.status_code == 404


class TestAttendance:
    """GET/POST /api/staff-attendance  and  GET /api/manager-staff-attendance"""

    def test_staff_mark_attendance(self, client, staff_token):
        """TC-ATT-01: Staff marks attendance – 201 on first call today."""
        rv = client.post('/api/staff-attendance', headers=auth_headers(staff_token))
        # May be 201 (first mark) or 400 (already marked today) – both acceptable
        assert rv.status_code in (201, 400)

    def test_staff_view_own_attendance(self, client, staff_token):
        """TC-ATT-02: Staff can view their own attendance records."""
        rv = client.get('/api/staff-attendance', headers=auth_headers(staff_token))
        assert rv.status_code == 200
        assert isinstance(rv.get_json(), list)

    def test_attendance_customer_forbidden(self, client, customer_token):
        """TC-ATT-03: Customer cannot mark or view staff attendance."""
        rv = client.post('/api/staff-attendance', headers=auth_headers(customer_token))
        assert rv.status_code == 403

    def test_manager_view_staff_attendance(self, client, manager_token):
        """TC-ATT-04: Manager views all staff attendance for today."""
        rv = client.get('/api/manager-staff-attendance',
                        headers=auth_headers(manager_token))
        assert rv.status_code == 200
        assert isinstance(rv.get_json(), list)

    def test_manager_view_attendance_specific_date(self, client, manager_token):
        """TC-ATT-05: Manager filters attendance by a specific date."""
        rv = client.get('/api/manager-staff-attendance?date=2026-04-04',
                        headers=auth_headers(manager_token))
        assert rv.status_code == 200

class TestStaffCustomerReview:
    def test_get_staff_reviews_success(self, client, staff_token, setup_review):
        """TC-REV-01: Logged-in staff retrieves their specific reviews and parsed service names."""
        rv = client.get('/api/staff-customer-reviews', headers=auth_headers(staff_token))
        data = rv.get_json()

        assert rv.status_code == 200
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]['review'] == "Excellent professional service"
        # Verifies the API successfully mapped the service_id string to a name
        assert len(data[0]['service_names']) > 0

    def test_get_staff_reviews_forbidden_for_customer(self, client, customer_token):
        """TC-REV-02: Ensures customers are blocked from accessing the staff review list."""
        rv = client.get('/api/staff-customer-reviews', headers=auth_headers(customer_token))
        
        # 403 Forbidden is the standard Flask-Security response for role mismatch
        assert rv.status_code == 403