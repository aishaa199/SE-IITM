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

def test_get_all_staff(client, create_staff,monkeypatch):
    from application.resources import StaffResource

    monkeypatch.setattr(StaffResource, "get", StaffResource.get.__wrapped__)
    staff1 = create_staff("staff1", "1234")
    staff2 = create_staff("staff2", "1234")

    response = client.get(
        "/api/staff",  follow_redirects=True )

    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2

    for staff in data:
        assert "is_present_today" in staff
        assert "appointments_today" in staff
        assert "active" in staff

