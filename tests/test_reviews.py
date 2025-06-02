def test_get_reviews(client):
    response = client.get("/reviews")
    assert response.status_code == 200
