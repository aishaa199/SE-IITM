def test_customer_cannot_create_service(client, customer_token):
    response = client.post("/api/service",
        json={"service_desc": "Test"},
        headers=customer_token
    )
    assert response.status_code == 403

def test_customer_cannot_access_manager_api(client, customer_token):
    res = client.post("/api/service",
        json={"service_desc": "Hack"},
        headers=customer_token
    )
    assert res.status_code == 403