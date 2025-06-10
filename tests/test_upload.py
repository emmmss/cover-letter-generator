import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_cover_letter_success(monkeypatch):
    # Patch at the route's import location
    def mock_save_and_index_text(text, user_id, category):
        return {"success": True, "doc_id": "mock_doc_id"}
    import app.routes.upload
    monkeypatch.setattr(app.routes.upload, "save_and_index_text", mock_save_and_index_text)

    response = client.post(
        "/upload-cover-letter",
        data={"user_id": "testuser", "past_letter_text": "This is a test letter."}
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["doc_id"] == "mock_doc_id"

def test_upload_cover_letter_error(monkeypatch):
    def mock_save_and_index_text(text, user_id, category):
        return {"error": "Some error"}
    import app.routes.upload
    monkeypatch.setattr(app.routes.upload, "save_and_index_text", mock_save_and_index_text)

    response = client.post(
        "/upload-cover-letter",
        data={"user_id": "testuser", "past_letter_text": "This is a test letter."}
    )
    assert response.status_code == 400
    assert "error" in response.json()
