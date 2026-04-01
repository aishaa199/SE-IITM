def create_sample_service(client, headers):
    return client.post(
        "/api/service",
        json={
            "service_desc": "Haircut",
            "service_category": "Hair",
            "service_price": 200,
            "service_duration": 30
        },
        headers=headers
    )



def create_sample_customer(client):
    return client.post(
        "/api/customer",
        json={
            "customer_name": "Test User",
            "customer_email": "test@test.com",
            "customer_phone": "9999999999"
        },
        follow_redirects=True
    )


def create_sample_staff(client):
    return client.post(
        "/api/staff",
        json={
            "staff_name": "John",
            "staff_email": "john@test.com",
            "staff_salary": 10000
        },
        follow_redirects=True
    )