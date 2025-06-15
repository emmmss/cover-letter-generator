import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import patch, MagicMock
from app.services import s3_handler

def test_save_text_to_s3_success(monkeypatch):
    # Mock s3_object_exists to always return False
    monkeypatch.setattr(s3_handler, "s3_object_exists", lambda bucket, key: False)
    # Mock s3.put_object to do nothing
    monkeypatch.setattr(s3_handler.s3, "put_object", lambda **kwargs: None)
    result = s3_handler.save_text_to_s3("test text", "user1", "cover_letter", "file.txt")
    assert result["success"] is True
    assert result["key"].endswith("file.txt")

def test_save_text_to_s3_duplicate(monkeypatch):
    monkeypatch.setattr(s3_handler, "s3_object_exists", lambda bucket, key: True)
    result = s3_handler.save_text_to_s3("test text", "user1", "cover_letter", "file.txt")
    assert "error" in result
    assert "already exists" in result["error"]

def test_save_text_to_s3_client_error(monkeypatch):
    class DummyError(Exception):
        def __init__(self):
            self.response = {"Error": {"Message": "fail!"}}
    def raise_client_error(*args, **kwargs):
        raise s3_handler.botocore.exceptions.ClientError({"Error": {"Code": "500", "Message": "fail!"}}, "PutObject")
    monkeypatch.setattr(s3_handler, "s3_object_exists", lambda bucket, key: False)
    monkeypatch.setattr(s3_handler.s3, "put_object", raise_client_error)
    result = s3_handler.save_text_to_s3("test text", "user1", "cover_letter", "file.txt")
    assert "error" in result
    assert "S3 ClientError" in result["error"]

def test_save_file_to_s3_success(monkeypatch):
    class DummyFile:
        file = None
        filename = "file.txt"
    monkeypatch.setattr(s3_handler, "s3_object_exists", lambda bucket, key: False)
    monkeypatch.setattr(s3_handler.s3, "upload_fileobj", lambda file, Bucket, Key: None)
    file = DummyFile()
    result = s3_handler.save_file_to_s3(file, "user1", "cover_letter")
    assert result["success"] is True
    assert result["key"].endswith("file.txt")

def test_get_text_from_s3_success(monkeypatch):
    class DummyBody:
        def read(self):
            return b"hello world"
    class DummyS3:
        def get_object(self, Bucket, Key):
            return {"Body": DummyBody()}
        class exceptions:
            class NoSuchKey(Exception):
                pass
    monkeypatch.setattr(s3_handler, "s3", DummyS3())
    result = s3_handler.get_text_from_s3("some/key.txt")
    assert result == "hello world"

def test_get_text_from_s3_no_such_key(monkeypatch):
    class DummyS3:
        class exceptions:
            class NoSuchKey(Exception):
                pass
        def get_object(self, Bucket, Key):
            raise DummyS3.exceptions.NoSuchKey()
    monkeypatch.setattr(s3_handler, "s3", DummyS3())
    result = s3_handler.get_text_from_s3("some/key.txt")
    assert result is None

