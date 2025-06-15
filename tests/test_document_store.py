import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import patch, MagicMock
from app.services import document_store

def test_save_and_index_text_success(monkeypatch):
    # Mock save_text_to_s3 to return a key
    monkeypatch.setattr(document_store, "save_text_to_s3", lambda text, user_id, category: {"key": "user1/cover_letter/abc.txt"})
    # Mock upsert_text to do nothing
    monkeypatch.setattr(document_store, "upsert_text", lambda text, record_id, user_id, metadata=None: None)
    result = document_store.save_and_index_text("test text", "user1", "cover_letter")
    assert result["success"] is True
    assert result["doc_id"] == "user1/cover_letter/abc.txt"

def test_save_and_index_text_error(monkeypatch):
    # Mock save_text_to_s3 to return an error
    monkeypatch.setattr(document_store, "save_text_to_s3", lambda text, user_id, category: {"error": "fail!"})
    result = document_store.save_and_index_text("test text", "user1", "cover_letter")
    assert "error" in result
    assert result["error"] == "fail!"

