
def test_ping(test_app, monkeypatch):
    response = test_app.get("/api/health-check")
    assert response.status_code == 200
    assert response.json() == {"msg": "hello"}