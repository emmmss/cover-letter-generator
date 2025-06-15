import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest

def test_refine_success(monkeypatch):
    class DummyResult:
        refined_letter = "Refined letter text"
    def mock_refine_cover_letter(payload):
        return DummyResult()
    import app.routes.refine
    monkeypatch.setattr(app.routes.refine, "refine_cover_letter", mock_refine_cover_letter)
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    payload = {
        "job_description": "Job desc",
        "original_letter": "Original letter",
        "feedback": "Feedback"
    }
    response = client.post("/refine", json=payload)
    assert response.status_code == 200
    assert response.json()["refined_letter"] == "Refined letter text"

def test_refine_error(monkeypatch):
    def mock_refine_cover_letter(payload):
        raise Exception("Refine error")
    import app.routes.refine
    monkeypatch.setattr(app.routes.refine, "refine_cover_letter", mock_refine_cover_letter)
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    payload = {
        "job_description": "Job desc",
        "original_letter": "Original letter",
        "feedback": "Feedback"
    }
    response = client.post("/refine", json=payload)
    assert response.status_code == 500
    assert "error" in response.json()
