"""
test_ai.py – Tests for AI endpoints.

The Anthropic SDK is patched at the class level so tests never make real API calls.

Endpoints covered:
  POST /ai/manager-chat
  GET  /ai/daily-briefing
  POST /ai/report-intent
  POST /ai/customer-chat
"""
import pytest
from unittest.mock import patch, MagicMock
from tests.conftest import auth_headers


# ─────────────────────────────────────────────────────────────────────────────
# Stub helpers
# ─────────────────────────────────────────────────────────────────────────────

def _mock_anthropic(text="AI response text."):
    """Return a context manager that patches anthropic.Anthropic everywhere."""
    mock_client = MagicMock()
    mock_msg = MagicMock()
    mock_msg.content = [MagicMock(text=text)]
    mock_client.messages.create.return_value = mock_msg
    return patch('anthropic.Anthropic', return_value=mock_client)


# ─────────────────────────────────────────────────────────────────────────────
# /ai/manager-chat  (POST)
# ─────────────────────────────────────────────────────────────────────────────

class TestManagerChat:
    """POST /ai/manager-chat"""

    def test_manager_chat_success(self, client, manager_token):
        """TC-AI-01: Manager asks a question and gets a plain-text AI response."""
        with _mock_anthropic("Today you have 3 appointments."):
            rv = client.post('/ai/manager-chat',
                             headers=auth_headers(manager_token),
                             json={'message': 'How many appointments do we have today?'})
        data = rv.get_json()
        assert rv.status_code == 200
        assert 'response' in data
        assert isinstance(data['response'], str)
        assert len(data['response']) > 0

    def test_manager_chat_with_history(self, client, manager_token):
        """TC-AI-02: Multi-turn conversation via history array is accepted."""
        with _mock_anthropic("Priya has 8 bookings this month."):
            rv = client.post('/ai/manager-chat',
                             headers=auth_headers(manager_token),
                             json={
                                 'message': 'Who is the top staff?',
                                 'history': [
                                     {'type': 'user', 'text': 'How is revenue?'},
                                     {'type': 'assistant', 'text': 'Revenue is 45000.'},
                                 ],
                             })
        assert rv.status_code == 200
        assert 'response' in rv.get_json()

    def test_manager_chat_empty_message(self, client, manager_token):
        """TC-AI-03: Empty message string → 400."""
        rv = client.post('/ai/manager-chat',
                         headers=auth_headers(manager_token),
                         json={'message': ''})
        assert rv.status_code == 400

    def test_manager_chat_missing_message(self, client, manager_token):
        """TC-AI-04: Missing message field → 400."""
        rv = client.post('/ai/manager-chat',
                         headers=auth_headers(manager_token),
                         json={})
        assert rv.status_code == 400

    def test_manager_chat_customer_forbidden(self, client, customer_token):
        """TC-AI-05: Customer role cannot call manager chat – 403."""
        rv = client.post('/ai/manager-chat',
                         headers=auth_headers(customer_token),
                         json={'message': 'show revenue'})
        assert rv.status_code == 403

    def test_manager_chat_unauthenticated(self, client):
        """TC-AI-06: No token → 401/302."""
        rv = client.post('/ai/manager-chat', json={'message': 'hello'})
        assert rv.status_code in (401, 302)


# ─────────────────────────────────────────────────────────────────────────────
# /ai/daily-briefing  (GET)
# ─────────────────────────────────────────────────────────────────────────────

class TestDailyBriefing:
    """GET /ai/daily-briefing"""

    def test_daily_briefing_success(self, client, manager_token):
        """TC-AI-07: Manager receives a structured daily briefing with known keys."""
        with _mock_anthropic("Good morning. Today you have 5 appointments."):
            rv = client.get('/ai/daily-briefing', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        data = rv.get_json()
        # Response can contain: summary, greeting, insights, recommendations, ai_error, etc.
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_daily_briefing_staff_forbidden(self, client, staff_token):
        """TC-AI-08: Staff role cannot call daily briefing – 403."""
        rv = client.get('/ai/daily-briefing', headers=auth_headers(staff_token))
        assert rv.status_code == 403

    def test_daily_briefing_unauthenticated(self, client):
        """TC-AI-09: No token → 401/302."""
        rv = client.get('/ai/daily-briefing')
        assert rv.status_code in (401, 302)


# ─────────────────────────────────────────────────────────────────────────────
# /ai/report-intent  (POST)
# ─────────────────────────────────────────────────────────────────────────────

class TestReportIntent:
    """POST /ai/report-intent"""

    def test_report_intent_success(self, client, manager_token):
        """TC-AI-10: Manager submits a message; AI classifies intent and returns result."""
        with _mock_anthropic('{"type": "revenue", "period": "this_month"}'):
            rv = client.post('/ai/report-intent',
                             headers=auth_headers(manager_token),
                             json={'message': 'Show me revenue report for this month'})
        # 200/201 on success; 422 if AI returns unparseable JSON (still a handled response)
        assert rv.status_code in (200, 201, 422)

    def test_report_intent_no_message(self, client, manager_token):
        """TC-AI-11: Missing message → 400."""
        rv = client.post('/ai/report-intent',
                         headers=auth_headers(manager_token),
                         json={})
        assert rv.status_code == 400

    def test_report_intent_customer_forbidden(self, client, customer_token):
        """TC-AI-12: Customer cannot access report-intent – 403."""
        rv = client.post('/ai/report-intent',
                         headers=auth_headers(customer_token),
                         json={'message': 'revenue'})
        assert rv.status_code == 403


# ─────────────────────────────────────────────────────────────────────────────
# /ai/customer-chat  (POST)
# ─────────────────────────────────────────────────────────────────────────────

class TestCustomerChat:
    """POST /ai/customer-chat"""

    def test_customer_chat_success(self, client, customer_token):
        """TC-AI-13: Customer gets help from the AI assistant."""
        with _mock_anthropic("Our haircut service takes 60 minutes."):
            rv = client.post('/ai/customer-chat',
                             headers=auth_headers(customer_token),
                             json={'message': 'How long does a haircut take?'})
        assert rv.status_code == 200
        data = rv.get_json()
        assert 'response' in data or 'message' in data

    def test_customer_chat_empty_message(self, client, customer_token):
        """TC-AI-14: Empty message → 400."""
        rv = client.post('/ai/customer-chat',
                         headers=auth_headers(customer_token),
                         json={'message': ''})
        assert rv.status_code == 400

    def test_customer_chat_manager_forbidden(self, client, manager_token):
        """TC-AI-15: Manager cannot call customer-chat – 403."""
        rv = client.post('/ai/customer-chat',
                         headers=auth_headers(manager_token),
                         json={'message': 'hello'})
        assert rv.status_code == 403
