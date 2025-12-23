from fastapi.testclient import TestClient
import sys
import os
from pathlib import Path

# Need to set this before importing main because it might use relative paths
# However, we appended sys.path in conftest.py
# We import the app from the service.
# Note: In the repo, the file is services/agent-creator/main.py.
# Since we added services/agent-creator to sys.path, we can just import main?
# No, multiple services have main.py. We need to be careful.
# We should import as a module if possible, or import from the full path.

# Let's try importing by finding the module spec or just appending and importing carefully.
# Given conftest.py appends all paths, `import main` is ambiguous.
# We should probably modify conftest to NOT append all paths, or import specifically.

# Better approach for this test file:
# Manually load the module from file path to avoid name collisions
import importlib.util

def load_service_app(service_name):
    file_path = Path(__file__).parent.parent / "services" / service_name / "main.py"
    spec = importlib.util.spec_from_file_location(f"{service_name}.main", file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"{service_name}.main"] = module
    spec.loader.exec_module(module)
    return module.app

client = TestClient(load_service_app("agent-creator"))

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "Agent Creator Service"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "agent-creator"}

def test_create_agent():
    # Test creating a valid agent
    agent_data = {
        "name": "Test Agent",
        "description": "A test agent",
        "system_prompt": "You are a test agent.",
        "model": "gpt-4"
    }
    response = client.post("/agents/create", json=agent_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == agent_data["name"]
    assert "agent_id" in data

    # Test creating invalid agent
    invalid_data = {
        "name": "Invalid Agent"
        # Missing description
    }
    response = client.post("/agents/create", json=invalid_data)
    assert response.status_code == 422
