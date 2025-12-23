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

client = TestClient(load_service_app("mcp-creator"))

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "MCP Creator Service"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "mcp-creator"}

def test_create_mcp_project():
    project_data = {
        "project_name": "Test Project",
        "description": "A test project",
        "base_path": "/api/v1",
        "resources": [
            {
                "name": "todo",
                "description": "A todo item",
                "fields": [
                    {
                        "name": "title",
                        "type": "string",
                        "required": True
                    },
                    {
                        "name": "completed",
                        "type": "boolean",
                        "required": False
                    }
                ]
            }
        ]
    }

    response = client.post("/mcp/create", json=project_data)
    assert response.status_code == 200
    data = response.json()
    assert data["project_name"] == "Test Project"
    assert "project_id" in data
    assert "download_url" in data
