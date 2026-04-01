from tests.utils import create_sample_service

def test_create_service(client):
    response = client.post(
        "/api/service",
        json={
            "service_desc": "Haircut",
            "service_category": "Hair",
            "service_price": 200,
            "service_duration": 30
        },
        follow_redirects=True
    )
    assert response.status_code == 201


def test_full_service_flow(client):
    res = create_sample_service(client)
    assert res.status_code == 201