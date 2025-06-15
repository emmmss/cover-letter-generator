import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import MagicMock
from app.services import pinecone_handler

def test_upsert_text(monkeypatch):
    # Mock index.upsert_records
    mock_index = MagicMock()
    monkeypatch.setattr(pinecone_handler, "index", mock_index)
    pinecone_handler.upsert_text("text", "id1", "user1", {"category": "cover_letter"})
    mock_index.upsert_records.assert_called_once()
    args, kwargs = mock_index.upsert_records.call_args
    assert kwargs["namespace"] == "user1"
    assert isinstance(kwargs["records"], list)
    assert kwargs["records"][0]["_id"] == "id1"
    assert kwargs["records"][0]["text"] == "text"
    assert kwargs["records"][0]["category"] == "cover_letter"

def test_get_similar_cover_letter_ids(monkeypatch):
    class DummyResult:
        hits = [{"_id": "id1"}, {"_id": "id2"}]
    class DummyMatches:
        result = DummyResult()
    mock_index = MagicMock()
    mock_index.search.return_value = DummyMatches()
    monkeypatch.setattr(pinecone_handler, "index", mock_index)
    ids = pinecone_handler.get_similar_cover_letter_ids("query", "user1", top_k=2)
    assert ids == ["id1", "id2"]
    mock_index.search.assert_called_once()

def test_get_similar_cover_letter_ids_empty(monkeypatch):
    class DummyMatches:
        result = type("DummyResult", (), {"hits": []})()
    mock_index = MagicMock()
    mock_index.search.return_value = DummyMatches()
    monkeypatch.setattr(pinecone_handler, "index", mock_index)
    ids = pinecone_handler.get_similar_cover_letter_ids("query", "user1", top_k=2)
    assert ids == []

