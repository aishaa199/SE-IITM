"""
test_daily_briefing.py – Tests for Daily Briefing API (/ai/daily-briefing).

Endpoints covered:
  GET /ai/daily-briefing (Daily AI Dashboard Briefing)
"""
import pytest
from tests.conftest import auth_headers

class TestDailyBriefing:
    """Tests for the daily briefing endpoint."""

    def test_daily_briefing_success(self, client, manager_token):
        """TC-DB-01: Manager can successfully fetch daily briefing (even if AI fails, fallback is tested)."""
        rv = client.get('/ai/daily-briefing', headers=auth_headers(manager_token))
        # Since call_claude_api might fail without real key/network, we expect 200 via fallback
        assert rv.status_code == 200
        data = rv.get_json()
        assert "greeting" in data
        assert "summary" in data
        assert "insights" in data
        assert "recommendations" in data
        assert isinstance(data['insights'], list)
        assert isinstance(data['recommendations'], list)

    def test_daily_briefing_owner_success(self, client, owner_token):
        """TC-DB-02: Owner can also fetch daily briefing."""
        rv = client.get('/ai/daily-briefing', headers=auth_headers(owner_token))
        assert rv.status_code == 200
        assert "greeting" in rv.get_json()

    def test_daily_briefing_forbidden_for_staff(self, client, staff_token):
        """TC-DB-03: Staff cannot access daily briefing."""
        rv = client.get('/ai/daily-briefing', headers=auth_headers(staff_token))
        assert rv.status_code == 403

    def test_daily_briefing_unauthenticated(self, client):
        """TC-DB-04: No token -> 401/302."""
        rv = client.get('/ai/daily-briefing')
        assert rv.status_code in (401, 302)
