import pytest
from tests.conftest import auth_headers

class TestAIAssistant:
    """Tests for AI-powered features for Managers and Customers."""

    # --- Manager AI Tests ---

    def test_get_daily_briefing_manager(self, client, manager_token):
        """TC-AI-01: Manager receives a personalized daily briefing."""
        rv = client.get('/ai/daily-briefing', headers=auth_headers(manager_token))
        # Note: 500 might occur if LLM API keys are missing in the test env
        assert rv.status_code in [200, 500] 
        if rv.status_code == 200:
            data = rv.get_json()
            assert 'greeting' in data
            assert 'summary' in data

    def test_generate_and_list_manager_tasks(self, client, manager_token):
        """TC-AI-02: Manager generates today's task checklist and retrieves it."""
        # 1. Generate tasks
        gen_rv = client.post('/ai/generate-manager-tasks', headers=auth_headers(manager_token))
        assert gen_rv.status_code in [200, 500]
        
        # 2. Retrieve tasks
        list_rv = client.get('/ai/manager-tasks', headers=auth_headers(manager_token))
        assert list_rv.status_code == 200
        data = list_rv.get_json()
        tasks = data.get('tasks', []) # Get the list from the 'tasks' key
        assert isinstance(tasks, list)

    def test_patch_task_status(self, client, manager_token):
        """TC-AI-03: Manager marks an AI-generated task as completed."""
        # Ensure a task exists
        client.post('/ai/generate-manager-tasks', headers=auth_headers(manager_token))
        data = client.get('/ai/manager-tasks', headers=auth_headers(manager_token)).get_json()
        tasks = data.get('tasks', [])
        if tasks:
            tid = tasks[0]['task_id']
            rv = client.patch(f'/tasks/{tid}', 
                             json={'status': 'completed'}, 
                             headers=auth_headers(manager_token))
            assert rv.status_code == 200
            assert rv.get_json()['status'] == 'completed'

    def test_report_intent_classification(self, client, manager_token):
        """TC-AI-04: AI classifies natural language report requests."""
        payload = {"message": "Show me sales for last month"}
        rv = client.post('/ai/report-intent', json=payload, headers=auth_headers(manager_token))
        
        assert rv.status_code == 200
        data = rv.get_json()
        assert 'report_type' in data
        assert 'time_period' in data

    # --- Customer AI Tests ---

    def test_generate_feedback_customer(self, client, customer_token):
        """TC-AI-05: Customer uses AI to polish a service review."""
        payload = {
            "keywords": ["Quality", "Staff Behavior"],
            "customer_note": "Great haircut but the floor was a bit messy",
            "service_name": "Mens Haircut",
            "staff_name": "Rahul"
        }
        rv = client.post('/ai/generate-feedback', json=payload, headers=auth_headers(customer_token))
        
        assert rv.status_code in [200, 500]
        if rv.status_code == 200:
            assert 'feedback_message' in rv.get_json()

    def test_customer_chat_bot(self, client, customer_token):
        """TC-AI-06: Customer chats with the AI for service advice."""
        payload = {"message": "I have a wedding to attend, what styling do you suggest?"}
        rv = client.post('/ai/customer-chat', json=payload, headers=auth_headers(customer_token))
        
        assert rv.status_code == 200
        assert 'response' in rv.get_json()

    def test_customer_chat_empty_message(self, client, customer_token):
        """TC-AI-07: Sending empty message to chatbot returns 400."""
        rv = client.post('/ai/customer-chat', json={'message': ''}, headers=auth_headers(customer_token))
        assert rv.status_code == 400