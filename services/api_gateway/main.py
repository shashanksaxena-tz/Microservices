import os
import httpx
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI(title="AI Microservices API Gateway")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY", "dev-api-key")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    import time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Path: {request.url.path} Method: {request.method} Status: {response.status_code} Duration: {process_time:.4f}s")
    return response

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    if request.url.path == "/health" or request.method == "OPTIONS":
        return await call_next(request)

    # Allow missing key for now for easier migration, but log warning
    # In production, uncomment the raise lines
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        # For now, just pass through to avoid breaking existing frontend which doesn't send key yet
        # raise HTTPException(status_code=403, detail="Missing API Key")
        pass
    elif api_key != API_KEY:
        return JSONResponse(
            status_code=403,
            content={"detail": "Invalid API Key"},
        )

    response = await call_next(request)
    return response

# Service URLs from environment variables (default to Docker Compose service names)
OCR_SERVICE_URL = os.getenv("OCR_SERVICE_URL", "http://ocr-service:8000")
AUDIO_SERVICE_URL = os.getenv("AUDIO_SERVICE_URL", "http://audio-service:8000")
AGENT_CREATOR_URL = os.getenv("AGENT_CREATOR_URL", "http://agent-creator:8000")
MCP_CREATOR_URL = os.getenv("MCP_CREATOR_URL", "http://mcp-creator:8000")
WHATSAPP_SERVICE_URL = os.getenv("WHATSAPP_SERVICE_URL", "http://whatsapp-service:8000")

SERVICES = {
    "ocr": OCR_SERVICE_URL,
    "audio": AUDIO_SERVICE_URL,
    "agent": AGENT_CREATOR_URL,
    "mcp": MCP_CREATOR_URL,
    "whatsapp": WHATSAPP_SERVICE_URL
}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "api-gateway"}

@app.api_route("/api/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(service_name: str, path: str, request: Request):
    """
    Proxy requests to the appropriate microservice.
    Example: /api/ocr/process -> ocr-service/process
    """
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")

    target_url = f"{SERVICES[service_name]}/{path}"

    # Forward query parameters
    params = dict(request.query_params)

    # Forward body
    content = await request.body()

    # Forward headers (excluding host to avoid confusion)
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None) # Let httpx handle content-length

    async with httpx.AsyncClient() as client:
        try:
            proxy_req = client.build_request(
                method=request.method,
                url=target_url,
                content=content,
                headers=headers,
                params=params,
                timeout=60.0
            )
            response = await client.send(proxy_req, stream=True)

            # Filter hop-by-hop headers
            excluded_headers = {'content-encoding', 'content-length', 'transfer-encoding', 'connection'}
            filtered_headers = {
                k: v for k, v in response.headers.items()
                if k.lower() not in excluded_headers
            }

            return StreamingResponse(
                response.aiter_bytes(),
                status_code=response.status_code,
                headers=filtered_headers,
                media_type=response.headers.get("content-type")
            )

        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"Error communicating with {service_name}: {str(exc)}")
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
