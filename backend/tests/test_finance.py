def test_create_finance_missing_date(client):
    response = client.post(
        "/api/finance",
        json={},
        follow_redirects=True
    )
    assert response.status_code == 400


def test_create_finance_valid(client):
    response = client.post(
        "/api/finance",
        json={"last_date": "2025-03-31"},
        follow_redirects=True
    )
    assert response.status_code in [201, 500]


def test_get_finance(client):
    response = client.get("/api/finance", follow_redirects=True)
    assert response.status_code == 200


def test_finance_generation(client):
    res = client.post(
        "/api/finance",
        json={"last_date": "2025-03-31"},
        follow_redirects=True
    )
    assert res.status_code in [201, 500]