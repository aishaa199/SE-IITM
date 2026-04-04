def test_get_finance(client):
    response = client.get("/api/finance", follow_redirects=True)
    assert response.status_code == 200

def test_generate_finance_report_success(client, manager_headers):
    # Setup - provide a valid month-end date
    payload = {"last_date": "2024-05-31"}

    response = client.post(
        "/api/finance",
        json=payload,
        headers=manager_headers
    )

    # Note: Check if your API returns 201 (Created) per your YAML
    assert response.status_code == 201
    data = response.get_json()
    assert "net_profit" in data
    assert "total_revenue" in data

def test_generate_finance_invalid_date_400(client, manager_headers):
    # Sending a string that isn't a YYYY-MM-DD date
    payload = {"last_date": "May-2024-31st"}

    response = client.post(
        "/api/finance",
        json=payload,
        headers=manager_headers
    )

    assert response.status_code == 400
    # Verify the error message mentions format
    assert "format" in str(response.get_json()).lower()

def test_prevent_duplicate_finance_report(client, manager_headers):
    payload = {"last_date": "2024-06-30"}

    # First generation
    first_res = client.post("/api/finance", json=payload, headers=manager_headers)
    assert first_res.status_code == 201

    # Second generation for the same month
    second_res = client.post("/api/finance", json=payload, headers=manager_headers)
    
    # Typically 400 (Bad Request) or 409 (Conflict)
    assert second_res.status_code in [400, 409]
    assert "already exists" in str(second_res.get_json()).lower()

def test_generate_finance_unauthorized_staff(client, staff_headers):
    payload = {"last_date": "2024-05-31"}

    # Staff should NOT be able to generate reports
    response = client.post(
        "/api/finance",
        json=payload,
        headers=staff_headers
    )

    # 403 Forbidden means they are logged in, but lack the 'manager'/'owner' role
    assert response.status_code == 403

def test_staff_cannot_access_finance_get(client, staff_headers):
    # Try to GET the finance list as a Staff member
    response = client.get("/api/finance", headers=staff_headers)
    
    # Should be 403 Forbidden
    assert response.status_code == 403
    
    # Try to POST a report as a Staff member
    response = client.post("/api/finance", json={"last_date": "2024-05-31"}, headers=staff_headers)
    assert response.status_code == 403
from datetime import datetime
from application.models import Appointment, Invoice, db

def test_finance_report_calculation_accuracy(client, manager_headers, create_customer, create_staff):
    # 1. Setup - We need the full chain
    cust = create_customer("fin_accuracy", "Finance User", "calc@test.com")
    stf = create_staff("fin_staff", "pass123")
    
    # 2. Create the Appointment
    appt = Appointment(
        customer_id=cust.customer_id,
        staff_id=stf.staff_id,
        appointment_datetime=datetime(2024, 5, 15, 10, 0),
        status=5  # Status 5 = Invoiced based on your model comment
    )
    db.session.add(appt)
    db.session.commit()

    # 3. Create the Invoice (This is where the money is!)
    inv = Invoice(
        customer_id=cust.customer_id,
        staff_id=stf.staff_id,
        appointment_id=appt.appointment_id,
        invoice_date=datetime(2024, 5, 15).date(),
        service_ids="1,2", # Dummy string
        invoice_amount=200.0,
        total_invoice_amount=200.0,
        payable_invoice_amount=180.0, # Let's say there was a discount
        status=1
    )
    db.session.add(inv)
    db.session.commit()

    # 4. Generate report for May
    payload = {"last_date": "2024-05-31"}
    response = client.post("/api/finance", json=payload, headers=manager_headers)
    
    assert response.status_code == 201
    data = response.get_json()

    # 5. Verify the math
    # Depending on your logic, it should pick up the 'payable_invoice_amount'
    assert data["total_revenue"] == 180.0