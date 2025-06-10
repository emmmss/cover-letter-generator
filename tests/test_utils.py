import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from fastapi import UploadFile
from app.utils import extract_text
from io import BytesIO

class DummyUploadFile:
    def __init__(self, filename, content):
        self.filename = filename
        self.file = BytesIO(content)

# Test .txt extraction
def test_extract_text_txt():
    file = DummyUploadFile("test.txt", b"Hello world!")
    assert extract_text(file) == "Hello world!"

# Test .pdf extraction (mock PyPDF2)
def test_extract_text_pdf(monkeypatch):
    class DummyPage:
        def extract_text(self):
            return "PDF text"
    class DummyPdfReader:
        pages = [DummyPage(), DummyPage()]
    monkeypatch.setattr("PyPDF2.PdfReader", lambda f: DummyPdfReader())
    file = DummyUploadFile("test.pdf", b"fakepdf")
    assert extract_text(file) == "PDF text PDF text"

# Test .docx extraction (mock docx)
def test_extract_text_docx(monkeypatch):
    class DummyParagraph:
        def __init__(self, text):
            self.text = text
    class DummyDoc:
        paragraphs = [DummyParagraph("Para1"), DummyParagraph("Para2")]
    monkeypatch.setattr("docx.Document", lambda f: DummyDoc())
    file = DummyUploadFile("test.docx", b"fakedocx")
    assert extract_text(file) == "Para1\nPara2"

# Test unsupported file type
def test_extract_text_unsupported():
    file = DummyUploadFile("test.xyz", b"data")
    with pytest.raises(ValueError):
        extract_text(file)

