def test_customer_summary(client):
    response = client.get("/api/customer-summary", follow_redirects=True)
    assert response.status_code in [200, 404]


def test_customer_upcoming(client):
    response = client.get("/api/customer-upcoming-appointments", follow_redirects=True)
    assert response.status_code in [200, 404]


def test_customer_history(client):
    response = client.get("/api/customer-history-appointments", follow_redirects=True)
    assert response.status_code in [200, 404]


def test_customer_summary_flow(client):
    res = client.get("/api/customer-summary", follow_redirects=True)
    assert res.status_code in [200, 404]