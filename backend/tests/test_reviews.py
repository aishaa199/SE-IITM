def test_get_pending_reviews(client):
    response = client.get("/api/customer-review", follow_redirects=True)
    assert response.status_code == 200


def test_submit_review_missing_fields(client):
    response = client.post(
        "/api/customer-review",
        json={},
        follow_redirects=True
    )
    assert response.status_code == 400


def test_review_flow(client):
    res = client.get("/api/customer-review", follow_redirects=True)
    assert res.status_code == 200

    res = client.post(
        "/api/customer-review",
        json={"appointment_id": 1, "rating": 5},
        follow_redirects=True
    )
    assert res.status_code in [201, 400, 404]