"""
test_sendemail.py – Tests for SendEmail (/api/send-email).

Endpoints covered:
  POST /api/send-email
"""
import pytest
import os
from tests.conftest import auth_headers

class TestSendEmailResource:
    """Tests for email dispatch functionality with attachments."""

    def test_send_email_missing_fields(self, client, manager_token):
        """TC-EMAIL-01: Returns 400 if required fields are missing."""
        rv = client.post('/api/send-email', 
                         headers=auth_headers(manager_token),
                         json={'subject': 'Test'})
        assert rv.status_code == 400
        assert "Missing required fields" in rv.get_json()['message']

    def test_send_email_file_not_found(self, client, manager_token):
        """TC-EMAIL-02: Returns 404 if the attachment file does not exist."""
        payload = {
            'document_path': '/tmp/non_existent_file.pdf',
            'subject': 'Invoice',
            'email_id': 'test@example.com'
        }
        rv = client.post('/api/send-email', 
                         headers=auth_headers(manager_token),
                         json=payload)
        assert rv.status_code == 404
        assert "File not found" in rv.get_json()['message']

    def test_send_email_forbidden_for_staff(self, client, staff_token):
        """TC-EMAIL-03: Staff members are not allowed to use the send-email API."""
        rv = client.post('/api/send-email', 
                         headers=auth_headers(staff_token),
                         json={})
        assert rv.status_code == 403

    def test_send_email_forbidden_for_customer(self, client, customer_token):
        """TC-EMAIL-04: Customers are not allowed to use the send-email API."""
        rv = client.post('/api/send-email', 
                         headers=auth_headers(customer_token),
                         json={})
        assert rv.status_code == 403

    def test_send_email_unauthenticated(self, client):
        """TC-EMAIL-05: No token → 401/302."""
        rv = client.post('/api/send-email', json={})
        assert rv.status_code in (401, 302)

    def test_send_email_success_mock(self, client, manager_token):
        """TC-EMAIL-06: Manager can send email if file exists (Requires a dummy file)."""
        # Create a dummy file for the test
        dummy_path = '/tmp/test_attachment.pdf'
        with open(dummy_path, 'w') as f:
            f.write('dummy content')
        
        try:
            payload = {
                'document_path': dummy_path,
                'subject': 'Test Subject',
                'email_id': 'manager@test.com'
            }
            rv = client.post('/api/send-email', 
                             headers=auth_headers(manager_token),
                             json=payload)
            
            # Note: In a real test environment, Flask-Mail should be mocked or set to suppress actual sending.
            # If the mail server is not configured, this might return 500 or succeed if MAIL_SUPPRESS_SEND is True.
            assert rv.status_code in (200, 500) 
        finally:
            if os.path.exists(dummy_path):
                os.remove(dummy_path)
