from fastapi.testclient import TestClient
from pathlib import Path
import importlib.util
import sys
from unittest.mock import patch, MagicMock

def load_service_app(service_name):
    file_path = Path(__file__).parent.parent / "services" / service_name / "main.py"
    spec = importlib.util.spec_from_file_location(f"{service_name}.main", file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"{service_name}.main"] = module
    spec.loader.exec_module(module)
    return module.app

# Since we mock fitz in conftest, loading the app should be safe
client = TestClient(load_service_app("ocr-service"))

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "OCR Service"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "ocr-service"}

# We can add more tests here that rely on the mocks
