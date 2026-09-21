from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_list_evals_returns_200():
    response = client.get("/evals")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_nonexistent_run_returns_404():
    response = client.get("/evals/99999")
    assert response.status_code == 404
