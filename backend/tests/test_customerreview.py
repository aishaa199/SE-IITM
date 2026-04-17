"""
test_customerreview.py – Tests for CustomerReviewResource (/api/customer-review).

Endpoints covered:
  GET /api/customer-review
  GET /api/customer-review/<invoice_number>
  POST /api/customer-review/<invoice_number>
"""
import pytest
from tests.conftest import auth_headers
from application.models import Invoice, Appointment, db

class TestCustomerReviewResource:
    """Tests for customer feedback system."""

    def test_get_pending_reviews_success(self, client, customer_token):
        """TC-REV-01: Customer can see pending reviews (appointments not yet reviewed)."""
        rv = client.get('/api/customer-review', headers=auth_headers(customer_token))
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert 'invoice_number' in data[0]
            assert 'appointment_id' in data[0]

    def test_get_pending_review_by_invoice_success(self, client, customer_token):
        """TC-REV-02: Customer can fetch details of a specific unreviewed invoice."""
        # First get all pending to find a valid invoice number
        all_rv = client.get('/api/customer-review', headers=auth_headers(customer_token))
        all_data = all_rv.get_json()
        
        if all_data:
            inv_num = all_data[0]['invoice_number']
            rv = client.get(f'/api/customer-review/{inv_num}', headers=auth_headers(customer_token))
            assert rv.status_code == 200
            assert rv.get_json()[0]['invoice_number'] == inv_num
        else:
            pytest.skip("No pending reviews found in dummy data for this customer")

    def test_post_review_missing_rating(self, client, customer_token):
        """TC-REV-03: Submitting review without rating returns 400."""
        rv = client.post('/api/customer-review/123', 
                         headers=auth_headers(customer_token),
                         json={'review': 'Great experience'})
        assert rv.status_code == 400
        assert "Rating is required" in rv.get_json()['message']

    def test_get_reviews_forbidden_for_staff(self, client, staff_token):
        """TC-REV-04: Staff cannot access customer review submission API."""
        rv = client.get('/api/customer-review', headers=auth_headers(staff_token))
        assert rv.status_code == 403

    def test_get_reviews_unauthenticated(self, client):
        """TC-REV-05: No token → 401/302."""
        rv = client.get('/api/customer-review')
        assert rv.status_code in (401, 302)
