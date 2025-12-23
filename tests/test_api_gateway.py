import pytest
from fastapi.testclient import TestClient
from services.api_gateway.main import app
import respx
from httpx import Response

client = TestClient(app)

@pytest.mark.asyncio
async def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "api-gateway"}

@pytest.mark.asyncio
@respx.mock
async def test_proxy_ocr_service():
    # Mock the downstream OCR service
    ocr_url = "http://ocr-service:8000/process"
    respx.post(ocr_url).mock(return_value=Response(200, json={"text": "extracted text"}))

    # Test the gateway proxy
    response = client.post("/api/ocr/process", json={"file": "dummy"}, headers={"X-API-Key": "dev-api-key"})

    assert response.status_code == 200
    assert response.json() == {"text": "extracted text"}
    assert respx.calls.call_count == 1
    assert respx.calls.last.request.url == ocr_url

@pytest.mark.asyncio
async def test_auth_invalid_key():
    response = client.post("/api/ocr/process", json={"file": "dummy"}, headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid API Key"

@pytest.mark.asyncio
@respx.mock
async def test_proxy_binary_content():
    # Mock download of a PDF
    ocr_url = "http://ocr-service:8000/download/test.pdf"
    pdf_content = b"%PDF-1.4..."
    respx.get(ocr_url).mock(return_value=Response(200, content=pdf_content, headers={"Content-Type": "application/pdf"}))

    response = client.get("/api/ocr/download/test.pdf", headers={"X-API-Key": "dev-api-key"})

    assert response.status_code == 200
    assert response.content == pdf_content
    assert response.headers["content-type"] == "application/pdf"

@pytest.mark.asyncio
@respx.mock
async def test_proxy_service_not_found():
    response = client.get("/api/invalid-service/resource")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

@pytest.mark.asyncio
@respx.mock
async def test_proxy_downstream_error():
    # Mock a downstream error
    audio_url = "http://audio-service:8000/transcribe"
    respx.post(audio_url).mock(return_value=Response(500, json={"detail": "Internal Server Error"}))

    response = client.post("/api/audio/transcribe")
    # Our gateway should forward the content, but the status code might be preserved or wrapped
    # The current implementation returns the response content and status code
    assert response.status_code == 500
