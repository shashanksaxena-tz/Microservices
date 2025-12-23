import sys
import os
from pathlib import Path
import pytest
from unittest.mock import MagicMock

# Mock heavy/external libraries that might not be in the test env
sys.modules["fitz"] = MagicMock()
sys.modules["pytesseract"] = MagicMock()
sys.modules["pdf2image"] = MagicMock()
sys.modules["PIL"] = MagicMock()
sys.modules["PIL.Image"] = MagicMock()
sys.modules["openai-whisper"] = MagicMock()
sys.modules["whisper"] = MagicMock()
sys.modules["pydub"] = MagicMock()

@pytest.fixture(autouse=True)
def mock_uploads_dir(monkeypatch, tmp_path):
    """Fixture to mock upload directories via environment variable."""
    uploads = tmp_path / "uploads"
    uploads.mkdir()
    (uploads / "agents").mkdir()
    (uploads / "audio").mkdir()
    (uploads / "mcp").mkdir()
    (uploads / "ocr").mkdir()
    (uploads / "whatsapp").mkdir()

    # Set the environment variable UPLOAD_DIR
    monkeypatch.setenv("UPLOAD_DIR", str(uploads))

    return uploads
