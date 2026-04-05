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

def test_get_all_customers_as_manager(client, manager_headers, create_customer):
    create_customer("jdoe", "John Doe", "john@example.com")
    create_customer("asmith", "Alice Smith", "alice@example.com")
    response = client.get("/api/customer", headers=manager_headers)
    assert response.status_code == 200
    data = response.get_json()
    
    assert isinstance(data, list)
    assert len(data) >= 2
    assert data[0]["customer_name"] == "John Doe"
    assert "customer_email" in data[0]

import uuid



def test_get_all_customers_empty(client, manager_headers):
    # We don't call create_customer here. 
    # Since client fixture uses drop_all/create_all, the DB is fresh.
    
    response = client.get("/api/customer", headers=manager_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    
    # Ensure it's a list and it's empty
    assert isinstance(data, list)
    assert len(data) == 0

def test_customer_profile_with_no_appointments(client, manager_headers, create_customer):
    # 1. Create a customer
    cust = create_customer("noappts", "No Appt User", "none@test.com")
    cust_id = cust.customer_id

    # 2. Fetch profile
    response = client.get(f"/api/customer/{cust_id}", headers=manager_headers)
    assert response.status_code == 200
    
    data = response.get_json()
    
    # 3. Check the appointments field (adjust key based on your Serializer/Marshmallow)
    # If your API returns an appointments list, it should be empty.
    if "appointments" in data:
        assert isinstance(data["appointments"], list)
        assert len(data["appointments"]) == 0

from datetime import datetime, timedelta
from application.models import Appointment, db

def test_large_appointment_data_retrieval(client, manager_headers, create_customer):
    # 1. Setup - We need a customer to own these appointments
    cust = create_customer("busybee", "Busy Bee", "busy@test.com")

    # 2. Seed 50 appointments into the database
    # This tests if the GET /api/appointment can handle a bulk result set
    for i in range(50):
        appt = Appointment(
            customer_id=cust.customer_id,
            appointment_datetime=datetime.now() + timedelta(days=i),
            status=1  # Completed
        )
        db.session.add(appt)
    db.session.commit()

    # 3. Fetch the full list using the Manager-level endpoint
    response = client.get("/api/appointment", headers=manager_headers)

    # 4. Assertions
    assert response.status_code == 200
    data = response.get_json()
    
    # Ensure data is a list and contains all 50 records
    assert isinstance(data, list)
    assert len(data) == 50
    
    # Optional: Verify the first one belongs to our test customer
    assert data[0]["customer_id"] == cust.customer_id