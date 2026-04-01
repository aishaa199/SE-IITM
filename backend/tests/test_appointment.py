from tests.utils import create_sample_customer, create_sample_service

def test_create_appointment_missing_fields(client):
    response = client.post("/api/appointment", json={}, follow_redirects=True)
    assert response.status_code == 400


def test_create_appointment_invalid_datetime(client):
    response = client.post("/api/appointment", json={
        "customer_email": "test@test.com",
        "service_ids": [1],
        "appointment_datetime": "wrong-format"
    }, follow_redirects=True)
    assert response.status_code == 400


def test_get_appointments(client):
    response = client.get("/api/appointment", follow_redirects=True)
    assert response.status_code == 200


def test_update_appointment_not_found(client):
    response = client.put(
        "/api/appointment/999",
        json={"status": 1},
        follow_redirects=True
    )
    assert response.status_code == 404


def test_delete_appointment(client):
    response = client.delete("/api/appointment/1", follow_redirects=True)
    assert response.status_code in [200, 404]


def test_create_appointment_success(client):
    create_sample_customer(client)
    create_sample_service(client)

    res = client.post("/api/appointment", json={
        "customer_email": "test@test.com",
        "service_ids": [1],
        "appointment_datetime": "2025-04-01T10:00:00"
    }, follow_redirects=True)

    assert res.status_code == 201


def test_appointment_invalid_service(client):
    create_sample_customer(client)

    res = client.post("/api/appointment", json={
        "customer_email": "test@test.com",
        "service_ids": [999],
        "appointment_datetime": "2025-04-01T10:00:00"
    }, follow_redirects=True)

    assert res.status_code == 400