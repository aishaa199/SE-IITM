"""
test_notifications.py – Tests for SendNotification (/api/send-notification).

Endpoints covered:
  POST /api/send-notification
  GET /api/send-notification (implicit search for unread)
"""
import pytest
from tests.conftest import auth_headers

class TestNotificationResource:
    """Tests for system notifications."""

    def test_send_notification_success(self, client, manager_token):
        """TC-NOTIF-01: Manager can successfully create a notification."""
        payload = {
            'subject': 'Appointment Update',
            'body': 'Your appointment has been rescheduled.',
            'phone_number': '1234567890'
        }
        rv = client.post('/api/send-notification', 
                         headers=auth_headers(manager_token),
                         json=payload)
        assert rv.status_code == 201
        data = rv.get_json()
        assert "Notification generated and saved successfully" in data['message']
        assert 'id' in data

    def test_send_notification_missing_fields(self, client, manager_token):
        """TC-NOTIF-02: Returns 400 if required fields are missing."""
        rv = client.post('/api/send-notification', 
                         headers=auth_headers(manager_token),
                         json={'subject': 'Only Subject'})
        assert rv.status_code == 400
        assert "Missing required fields" in rv.get_json()['message']

    def test_send_notification_customer_success(self, client, customer_token):
        """TC-NOTIF-03: Customer can also create a notification (e.g. support request)."""
        payload = {
            'subject': 'Feedback',
            'body': 'I loved the service today!',
            'phone_number': '9876543210'
        }
        rv = client.post('/api/send-notification', 
                         headers=auth_headers(customer_token),
                         json=payload)
        assert rv.status_code == 201

    def test_get_notifications_authenticated(self, client, staff_token):
        """TC-NOTIF-04: Logged-in user can retrieve their notifications."""
        rv = client.get('/api/send-notification', headers=auth_headers(staff_token))
        assert rv.status_code == 200
        assert isinstance(rv.get_json(), list)

    def test_notification_unauthenticated(self, client):
        """TC-NOTIF-05: No token → 401/302."""
        rv = client.post('/api/send-notification', json={})
        assert rv.status_code in (401, 302)
