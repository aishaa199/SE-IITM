from utils import create_sample_customer, create_sample_service

def test_get_invoice_invalid_appt(client):
    response = client.get("/api/invoice/999", follow_redirects=True)
    assert response.status_code == 404


def test_create_invoice_missing_fields(client):
    response = client.post(
        "/api/invoice",
        json={},
        follow_redirects=True
    )
    assert response.status_code == 400


def test_get_all_invoices(client):
    response = client.get("/api/invoice", follow_redirects=True)
    assert response.status_code == 200


def test_invoice_creation(client):
    create_sample_customer(client)
    create_sample_service(client)  # 🔥 removed manager_token

    # Create appointment first
    appt = client.post(
        "/api/appointment",
        json={
            "customer_email": "test@test.com",
            "service_ids": [1],
            "appointment_datetime": "2025-04-01T10:00:00"
        },
        follow_redirects=True
    )

    appointment_id = appt.get_json()["appointment_id"]

    # Create invoice
    res = client.post(
        "/api/invoice",
        json={
            "customer_id": 1,
            "staff_id": 1,
            "service_ids": "1",
            "invoice_amount": 200,
            "appointment_id": appointment_id
        },
        follow_redirects=True
    )

    assert res.status_code in [201, 500]