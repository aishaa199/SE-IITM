
def test_create_invoice_missing_fields_400(client, manager_headers):
    # Sending an empty JSON object
    response = client.post(
        "/api/invoice",
        json={},
        headers=manager_headers
    )
    
    # 1. Check status code
    assert response.status_code == 400
    
    # 2. Verify that the error message points to required fields
    data = response.get_json()
    # If using reqparse, it usually puts errors in 'message'
    # If using custom logic, adjust the key accordingly
    error_str = str(data).lower()
    assert "customer_id" in error_str or "required" in error_str


def test_get_all_invoices(client):
    response = client.get("/api/invoice", follow_redirects=True)
    assert response.status_code == 200

def test_create_invoice_success(client, manager_headers, create_customer, create_staff):
    # 1. Setup - Invoice needs an existing customer, staff, and appointment
    cust = create_customer("inv_user", "Invoice User", "inv@test.com")
    stf = create_staff("inv_staff", "pass")
    
    from application.models import Appointment, db
    appt = Appointment(customer_id=cust.customer_id, staff_id=stf.staff_id, 
                       appointment_datetime=db.func.now(), status=0)
    db.session.add(appt)
    db.session.commit()

    # 2. Payload matching your Invoice model
    payload = {
        "customer_id": cust.customer_id,
        "staff_id": stf.staff_id,
        "appointment_id": appt.appointment_id,
        "service_ids": "1,2,3",
        "invoice_amount": 500.0,
        "total_invoice_amount": 500.0,
        "payable_invoice_amount": 500.0,
        "rewards_earned": 50
    }

    response = client.post("/api/invoice", json=payload, headers=manager_headers)
    assert response.status_code == 201
    assert "invoice_number" in response.get_json()

def test_create_invoice_invalid_appointment_404(client, manager_headers, create_customer, create_staff):
    cust = create_customer("bad_appt", "Bad Appt", "bad@test.com")
    stf = create_staff("bad_stf", "pass")

    payload = {
        "customer_id": cust.customer_id,
        "staff_id": stf.staff_id,
        "appointment_id": "sa5",  # Non-existent ID
        "service_ids": "1",
        "invoice_amount": 100.0,
        "total_invoice_amount": 100.0,
        "payable_invoice_amount": 100.0
    }

    response = client.post("/api/invoice", json=payload, headers=manager_headers)
    assert response.status_code == 404

def test_create_invoice_bad_service_format(client, manager_headers):
    # Sending an object instead of a string for service_ids
    payload = {
        "service_ids": {"id": 1},  # Should be "1"
        "invoice_amount": 100.0
    }
    response = client.post("/api/invoice", json=payload, headers=manager_headers)
    assert response.status_code == 400

# test reward logic here

def test_get_past_months_list(client, manager_headers, create_customer, create_staff):
    from application.models import Invoice, db
    from datetime import datetime
    
    # 1. Manually seed an invoice for February
    cust = create_customer("month_user", "Month", "m@test.com")
    stf = create_staff("month_stf", "pass")
    
    inv = Invoice(
        customer_id=cust.customer_id,
        staff_id=stf.staff_id,
        service_ids="1",
        invoice_date=datetime(2024, 2, 15).date(),
        invoice_amount=100.0,
        total_invoice_amount=100.0,
        payable_invoice_amount=100.0
    )
    db.session.add(inv)
    db.session.commit()

    # 2. Call the endpoint
    response = client.get("/api/past-months", headers=manager_headers)
    assert response.status_code == 200
    
    months = response.get_json()
    # Expecting something like ["2024-02"] or ["February 2024"]
    assert any("2024-02" in m for m in months)