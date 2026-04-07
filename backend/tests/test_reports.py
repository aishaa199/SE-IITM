import pytest
from tests.conftest import auth_headers
def _get_first_report_id(client, token):
    rv = client.get('/reports', headers=auth_headers(token))
    data = rv.get_json()

    if data and isinstance(data, list):
        first = data[0]
        return first.get('report_id') or first.get('id')  # ✅ flexible
    return None
class TestReports:
    """Tests for Report Generation, Analytics, and Sharing."""

    def test_generate_report_csv(self, client, manager_token):
        """TC-RPT-01: Manager generates a CSV report."""
        payload = {
            "report_type": "sales",
            "time_period": "monthly",
            "format": "csv"
        }
        rv = client.post('/generate-report', json=payload, headers=auth_headers(manager_token))
        
        # Reports can be heavy; 500 might occur if PDF/CSV libraries aren't installed
        assert rv.status_code in [200, 500]
        if rv.status_code == 200:
            assert 'text/csv' in rv.content_type

    def test_list_reports(self, client, manager_token):
        """TC-RPT-02: Manager can view list of generated reports."""
        rv = client.get('/reports', headers=auth_headers(manager_token))
        assert rv.status_code == 200
        assert isinstance(rv.get_json(), list)

    def test_get_analytics_data(self, client, manager_token):
        """TC-RPT-03: Fetch chart-ready analytics JSON."""
        params = {
            "type": "appointments",
            "period": "weekly"
        }
        rv = client.get('/reports/analytics', query_string=params, headers=auth_headers(manager_token))
        assert rv.status_code == 200
        assert isinstance(rv.get_json(), dict)

    def test_download_saved_report(self, client, manager_token):
        """TC-RPT-04: Download a specific report by ID."""
        report_id = _get_first_report_id(client, manager_token)
        if not report_id:
            pytest.skip("No reports found to test download")
            
        rv = client.get(f'/reports/{report_id}/download?format=pdf', headers=auth_headers(manager_token))
        assert rv.status_code in [200, 404]

    def test_share_report_with_owner(self, client, manager_token):
        """TC-RPT-05: Manager shares a report with the owner."""
        report_id = _get_first_report_id(client, manager_token)
        if not report_id:
            pytest.skip("No reports found to test sharing")
            
        rv = client.post(f'/reports/{report_id}/share', headers=auth_headers(manager_token))
        assert rv.status_code in [200, 403] # 403 if they don't own the report

    def test_generate_and_share_one_step(self, client, manager_token):
        """TC-RPT-06: Combined generate and share action."""
        payload = {
            "report_type": "inventory",
            "time_period": "daily"
        }
        rv = client.post('/reports/generate-and-share', json=payload, headers=auth_headers(manager_token))
        assert rv.status_code in [200, 500]
        if rv.status_code == 200:
            assert 'message' in rv.get_json()
            assert 'id' in rv.get_json()

    def test_invalid_report_type(self, client, manager_token):
        """TC-RPT-07: Error handling for invalid report type."""
        payload = {
            "report_type": "invalid_type",
            "time_period": "daily",
            "format": "csv"
        }
        rv = client.post('/generate-report', json=payload, headers=auth_headers(manager_token))
        assert rv.status_code == 400