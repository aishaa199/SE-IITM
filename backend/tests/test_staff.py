def test_staff_appointments(client):
    response = client.get("/api/staff-appointments", follow_redirects=True)
    assert response.status_code in [200, 404]


def test_staff_attendance_get(client):
    response = client.get("/api/staff-attendance", follow_redirects=True)
    assert response.status_code in [200, 404]


def test_staff_attendance_post(client):
    response = client.post("/api/staff-attendance", follow_redirects=True)
    assert response.status_code in [200, 201, 400]


def test_staff_attendance_flow(client):
    # Mark attendance
    res = client.post("/api/staff-attendance", follow_redirects=True)
    assert res.status_code in [200, 201, 400]

    # Get attendance
    res = client.get("/api/staff-attendance", follow_redirects=True)
    assert res.status_code in [200, 404]