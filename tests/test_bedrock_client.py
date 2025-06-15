import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import patch, MagicMock
from app.services import bedrock_client

def test_generate_from_bedrock(monkeypatch):
    mock_response = {
        "output": {
            "message": {
                "content": [
                    {"text": "Generated text"}
                ]
            }
        }
    }
    monkeypatch.setattr(bedrock_client.bedrock, "converse", lambda **kwargs: mock_response)
    result = bedrock_client.generate_from_bedrock("Prompt text")
    assert result == "Generated text"

def test_get_embedding(monkeypatch):
    class DummyBody:
        def read(self):
            return b'{"embedding": [0.1, 0.2, 0.3]}'
    mock_response = {"body": DummyBody()}
    monkeypatch.setattr(bedrock_client.bedrock, "invoke_model", lambda **kwargs: mock_response)
    embedding = bedrock_client.get_embedding("Some text")
    assert embedding == [0.1, 0.2, 0.3]

