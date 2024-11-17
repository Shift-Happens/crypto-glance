def test_home_page():
    from main import app
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200