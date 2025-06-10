import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_cover_letter_success(monkeypatch):
    # Mock all external dependencies
    import app.routes.generate
    monkeypatch.setattr(app.routes.generate, "get_similar_cover_letter_ids", lambda query, user_id, top_k=3: ["doc1", "doc2"])
    monkeypatch.setattr(app.routes.generate, "get_text_from_s3", lambda key: "Example cover letter text")
    monkeypatch.setattr(app.routes.generate, "save_and_index_text", lambda text, user_id, category: {"success": True, "doc_id": "mock_doc_id"})
    monkeypatch.setattr(app.routes.generate, "extract_text", lambda file: "Extracted CV text")
    monkeypatch.setattr(app.routes.generate, "build_prompt", lambda cv_text, job_description, past_letter_text: "Prompt text")
    monkeypatch.setattr(app.routes.generate, "generate_from_bedrock", lambda prompt: "Generated cover letter")

    with open("/tmp/test_cv.txt", "w") as f:
        f.write("CV content")
    with open("/tmp/test_cv.txt", "rb") as f:
        response = client.post(
            "/generate",
            data={"user_id": "testuser", "job_description": "Job desc", "past_letter_text": "Past letter"},
            files={"cv": ("test_cv.txt", f, "text/plain")}
        )
    assert response.status_code == 200
    assert "cover_letter" in response.json()
    assert response.json()["cover_letter"] == "Generated cover letter"

def test_generate_cover_letter_error(monkeypatch):
    import app.routes.generate
    def raise_exception(*args, **kwargs):
        raise Exception("Test error")
    monkeypatch.setattr(app.routes.generate, "get_similar_cover_letter_ids", raise_exception)

    with open("/tmp/test_cv.txt", "w") as f:
        f.write("CV content")
    with open("/tmp/test_cv.txt", "rb") as f:
        response = client.post(
            "/generate",
            data={"user_id": "testuser", "job_description": "Job desc", "past_letter_text": "Past letter"},
            files={"cv": ("test_cv.txt", f, "text/plain")}
        )
    assert response.status_code == 500
    assert "error" in response.json()

