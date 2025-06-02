def test_register_and_login(client):
    response = client.post("/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 201

    response = client.post("/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.get_json()
