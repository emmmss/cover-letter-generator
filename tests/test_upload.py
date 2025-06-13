import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from fastapi.testclient import TestClient
from app.main import app as fastapi_app
import app.routes.upload
from app.routes.upload import get_current_user

client = TestClient(fastapi_app)

def dummy_user():
    return {"sub": "test-user", "email": "test@example.com"}

def test_upload_cover_letter_success(monkeypatch):
    # Patch save_and_index_text to avoid real S3/Pinecone calls
    def mock_save_and_index_text(text, user_id, category):
        return {"success": True, "doc_id": "mock_doc_id"}
    monkeypatch.setattr(app.routes.upload, "save_and_index_text", mock_save_and_index_text)
    # Use dependency override for authentication
    fastapi_app.dependency_overrides[get_current_user] = dummy_user

    response = client.post(
        "/upload-cover-letter",
        data={"user_id": "testuser", "past_letter_text": "This is a test letter."}
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["doc_id"] == "mock_doc_id"
    # Clean up dependency override
    fastapi_app.dependency_overrides = {}

def test_upload_cover_letter_error(monkeypatch):
    def mock_save_and_index_text(text, user_id, category):
        return {"error": "Some error"}
    monkeypatch.setattr(app.routes.upload, "save_and_index_text", mock_save_and_index_text)
    # Use dependency override for authentication
    fastapi_app.dependency_overrides[get_current_user] = dummy_user

    response = client.post(
        "/upload-cover-letter",
        data={"user_id": "testuser", "past_letter_text": "This is a test letter."}
    )
    assert response.status_code == 400
    assert "error" in response.json()
    # Clean up dependency override
    fastapi_app.dependency_overrides = {}
