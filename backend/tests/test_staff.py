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

from datetime import datetime

def test_get_attendance_success_200(client, manager_headers, create_staff, create_attendance):
    # 1. Setup - Create staff and mark them present
    s1 = create_staff("present_staff1", "pass")
    s2 = create_staff("present_staff2", "pass")
    
    today_str = datetime.now().strftime('%Y-%m-%d')
    create_attendance(s1.staff_id, datetime.now())
    create_attendance(s2.staff_id, datetime.now())

    # 2. Fetch via Manager endpoint with date query param
    response = client.get(
        f"/api/manager-staff-attendance?date={today_str}",
        headers=manager_headers
    )

    # 3. Assertions
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2
    # Verify the structure matches your StaffAttendance schema
    assert "staff_id" in data[0]

def test_get_attendance_empty_404(client, manager_headers):
    # Search for a date far in the future
    future_date = "2099-12-31"
    
    response = client.get(
        f"/api/manager-staff-attendance?date={future_date}",
        headers=manager_headers
    )

    assert response.status_code == 404
    data = response.get_json()
    # Usually, 404s have an error message in the response
    assert "message" in data or "errors" in data

def test_get_attendance_invalid_format_400(client, manager_headers):
    # Pass an invalid date format (DD-MM-YYYY instead of YYYY-MM-DD)
    bad_date = "31-12-2024"
    
    response = client.get(
        f"/api/manager-staff-attendance?date={bad_date}",
        headers=manager_headers
    )

    assert response.status_code == 400
    # Verify that the API explains the error
    data = response.get_json()
    assert "Invalid date format" in str(data)


def test_prevent_double_attendance_400(client, staff_headers, create_staff):
    # 1. Setup - Create a staff member
    # Note: Use staff_headers because staff usually mark their own attendance
    s1 = create_staff("testcheckin", "password123")
    
    # 2. First Mark: Success (201 Created or 200 OK)
    # Adjust the payload based on your Appointment/Attendance schema
    payload = {
        "staff_id": s1.staff_id,
        "date": datetime.now().strftime('%Y-%m-%d')
    }
    
    first_res = client.post("/api/staff-attendance", json=payload, headers=staff_headers)
    assert first_res.status_code in [200, 201]

    # 3. Second Mark: Failure (400 Bad Request)
    # Sending the exact same data for the same day
    second_res = client.post("/api/staff-attendance", json=payload, headers=staff_headers)
    
    assert second_res.status_code == 400
    
    # 4. Verify the error message
    data = second_res.get_json()
    assert "already exists" in str(data).lower() or "already marked" in str(data).lower()