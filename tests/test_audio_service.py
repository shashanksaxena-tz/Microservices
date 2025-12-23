from fastapi.testclient import TestClient
from pathlib import Path
import importlib.util
import sys

def load_service_app(service_name):
    file_path = Path(__file__).parent.parent / "services" / service_name / "main.py"
    spec = importlib.util.spec_from_file_location(f"{service_name}.main", file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"{service_name}.main"] = module
    spec.loader.exec_module(module)
    return module.app

client = TestClient(load_service_app("audio-service"))

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "Audio Transcription Service"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "audio-service"}
