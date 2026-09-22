def test_create_vendor(client):
    payload = {
        "name": "Test Automation Vendor",
        "gst_number": "27TESTAUTO001",
        "email": "testautomation@example.com",
        "phone": "9999990001",
        "address": "Pune, Maharashtra"
    }

    response = client.post("/vendors/", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == payload["name"]
    assert data["gst_number"] == payload["gst_number"]
    assert data["email"] == payload["email"]
    assert data["phone"] == payload["phone"]
    assert data["address"] == payload["address"]