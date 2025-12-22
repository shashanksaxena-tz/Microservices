# API Documentation

Complete API reference for all microservices in the platform.

## Table of Contents
1. [OCR Service](#ocr-service)
2. [Audio Transcription Service](#audio-transcription-service)
3. [Agent Creator Service](#agent-creator-service)
4. [MCP Creator Service](#mcp-creator-service)
5. [WhatsApp Integration Service](#whatsapp-integration-service)

---

## OCR Service

**Base URL:** `http://localhost:8001`

### Endpoints

#### 1. Extract Text from PDF
Extract text with coordinates from a PDF file.

**Endpoint:** `POST /ocr/extract`

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `file`: PDF file (required)

**Response:**
```json
{
  "file_id": "uuid",
  "filename": "document.pdf",
  "extraction": {
    "pages": [
      {
        "page_number": 1,
        "width": 595.0,
        "height": 842.0,
        "blocks": [
          {
            "text": "Sample text",
            "bbox": [x1, y1, x2, y2],
            "size": 12.0,
            "font": "Arial"
          }
        ]
      }
    ],
    "total_pages": 1
  }
}
```

#### 2. Highlight PDF
Create a highlighted PDF with search terms marked.

**Endpoint:** `POST /ocr/highlight`

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `file`: PDF file (required)
  - `search_terms`: Comma-separated search terms (required)

**Response:**
```json
{
  "file_id": "uuid",
  "filename": "document.pdf",
  "highlighted_file": "uuid_highlighted.pdf",
  "search_terms": ["term1", "term2"],
  "download_url": "/ocr/download/uuid_highlighted.pdf"
}
```

#### 3. Download Highlighted PDF
Download a processed PDF file.

**Endpoint:** `GET /ocr/download/{filename}`

**Response:** PDF file download

---

## Audio Transcription Service

**Base URL:** `http://localhost:8002`

### Endpoints

#### 1. Transcribe Audio
Transcribe an audio file with timestamps.

**Endpoint:** `POST /audio/transcribe`

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `file`: Audio file (MP3, WAV, M4A, OGG, FLAC) (required)

**Response:**
```json
{
  "file_id": "uuid",
  "filename": "audio.mp3",
  "transcription": {
    "text": "Full transcription text",
    "language": "en",
    "segments": [
      {
        "id": 0,
        "start": 0.0,
        "end": 5.5,
        "text": "Segment text",
        "words": []
      }
    ]
  }
}
```

#### 2. Transcribe with Highlights
Transcribe audio and highlight specific keywords.

**Endpoint:** `POST /audio/highlight`

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `file`: Audio file (required)
  - `keywords`: Comma-separated keywords (required)

**Response:**
```json
{
  "file_id": "uuid",
  "filename": "audio.mp3",
  "transcription": { ... },
  "highlights": [
    {
      "keyword": "meeting",
      "segment_id": 0,
      "start": 10.5,
      "end": 15.0,
      "text": "Segment containing keyword",
      "context": "Full context text"
    }
  ],
  "keywords": ["meeting", "action"]
}
```

#### 3. Get Result
Retrieve transcription or highlight result by file ID.

**Endpoint:** `GET /audio/result/{file_id}`

**Response:** Transcription or highlight result object

---

## Agent Creator Service

**Base URL:** `http://localhost:8003`

### Endpoints

#### 1. Create Agent
Create a new AI agent configuration.

**Endpoint:** `POST /agents/create`

**Request:**
```json
{
  "name": "Customer Support Agent",
  "description": "Handles customer queries",
  "system_prompt": "You are a helpful support agent...",
  "model": "gpt-4",
  "temperature": 0.7,
  "tools": [
    {
      "name": "search",
      "description": "Search knowledge base",
      "parameters": {}
    }
  ],
  "capabilities": ["text-understanding", "response-generation"]
}
```

**Response:**
```json
{
  "agent_id": "uuid",
  "name": "Customer Support Agent",
  "description": "Handles customer queries",
  "created_at": "2024-01-01T00:00:00",
  "config": { ... }
}
```

#### 2. List Agents
Get all created agents.

**Endpoint:** `GET /agents/list`

**Response:**
```json
{
  "agents": [
    {
      "agent_id": "uuid",
      "name": "Agent Name",
      "description": "Agent description",
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 1
}
```

#### 3. Get Agent
Get specific agent configuration.

**Endpoint:** `GET /agents/{agent_id}`

**Response:**
```json
{
  "id": "uuid",
  "config": {
    "name": "Agent Name",
    "description": "Description",
    "model": "gpt-4",
    "temperature": 0.7,
    "system_prompt": "...",
    "tools": [],
    "capabilities": []
  }
}
```

#### 4. Update Agent
Update agent configuration.

**Endpoint:** `PUT /agents/{agent_id}`

**Request:** Same as create agent

**Response:** Updated agent configuration

#### 5. Delete Agent
Delete an agent.

**Endpoint:** `DELETE /agents/{agent_id}`

**Response:**
```json
{
  "message": "Agent deleted successfully"
}
```

#### 6. List Templates
Get available agent templates.

**Endpoint:** `GET /agents/templates/list`

**Response:**
```json
{
  "templates": [
    {
      "id": "customer-support",
      "name": "Customer Support Agent",
      "description": "Template description",
      "capabilities": ["text-understanding"]
    }
  ]
}
```

#### 7. Create from Template
Create agent from template.

**Endpoint:** `POST /agents/templates/{template_id}`

**Response:** Created agent configuration

---

## MCP Creator Service

**Base URL:** `http://localhost:8004`

### Endpoints

#### 1. Create MCP Project
Generate a complete CRUD API project.

**Endpoint:** `POST /mcp/create`

**Request:**
```json
{
  "project_name": "User Management API",
  "description": "API for managing users",
  "base_path": "/api/v1",
  "resources": [
    {
      "name": "user",
      "description": "User resource",
      "fields": [
        {
          "name": "name",
          "type": "string",
          "required": true,
          "description": "User's full name"
        },
        {
          "name": "email",
          "type": "string",
          "required": true,
          "description": "User's email"
        },
        {
          "name": "age",
          "type": "integer",
          "required": false,
          "description": "User's age"
        }
      ],
      "enable_create": true,
      "enable_read": true,
      "enable_update": true,
      "enable_delete": true,
      "enable_list": true
    }
  ]
}
```

**Response:**
```json
{
  "project_id": "uuid",
  "project_name": "User Management API",
  "description": "API for managing users",
  "files_generated": ["main.py", "Dockerfile", "requirements.txt", "metadata.json"],
  "download_url": "/mcp/download/uuid",
  "metadata": { ... }
}
```

#### 2. List Projects
Get all created MCP projects.

**Endpoint:** `GET /mcp/list`

**Response:**
```json
{
  "projects": [
    {
      "project_id": "uuid",
      "project_name": "User Management API",
      "description": "API description",
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 1
}
```

#### 3. Get Project
Get project details and files.

**Endpoint:** `GET /mcp/{project_id}`

**Response:**
```json
{
  "project_id": "uuid",
  "metadata": { ... },
  "files": {
    "main.py": "# Generated code...",
    "Dockerfile": "FROM python:3.11...",
    "requirements.txt": "fastapi==0.109.0..."
  }
}
```

#### 4. Get Generated Code
Get just the generated code for a project.

**Endpoint:** `GET /mcp/code/{project_id}`

**Response:**
```json
{
  "project_id": "uuid",
  "code": "# Full generated FastAPI code..."
}
```

#### 5. Delete Project
Delete an MCP project.

**Endpoint:** `DELETE /mcp/{project_id}`

**Response:**
```json
{
  "message": "Project deleted successfully"
}
```

---

## WhatsApp Integration Service

**Base URL:** `http://localhost:8005`

### Endpoints

#### 1. Send Text Message
Send a text message via WhatsApp.

**Endpoint:** `POST /whatsapp/send/text`

**Request:**
```json
{
  "to": "+1234567890",
  "message": "Hello from the platform!"
}
```

**Response:**
```json
{
  "status": "sent",
  "to": "+1234567890",
  "message": "Hello from the platform!",
  "response": {
    "messaging_product": "whatsapp",
    "contacts": [...],
    "messages": [...]
  }
}
```

#### 2. Send Template Message
Send a WhatsApp template message.

**Endpoint:** `POST /whatsapp/send/template`

**Request:**
```json
{
  "to": "+1234567890",
  "template_name": "hello_world",
  "language_code": "en"
}
```

**Response:**
```json
{
  "status": "sent",
  "to": "+1234567890",
  "template": "hello_world",
  "response": { ... }
}
```

#### 3. Send Media Message
Send media (image, video, audio, document) via WhatsApp.

**Endpoint:** `POST /whatsapp/send/media`

**Request:**
```json
{
  "to": "+1234567890",
  "media_type": "image",
  "media_url": "https://example.com/image.jpg",
  "caption": "Optional caption"
}
```

**Response:**
```json
{
  "status": "sent",
  "to": "+1234567890",
  "media_type": "image",
  "response": { ... }
}
```

#### 4. Webhook Verification
Verify WhatsApp webhook (GET request from WhatsApp).

**Endpoint:** `GET /whatsapp/webhook`

**Query Parameters:**
- `hub.mode`: subscribe
- `hub.verify_token`: Your verification token
- `hub.challenge`: Challenge string

**Response:** Challenge number (integer)

#### 5. Webhook Receive
Receive WhatsApp webhook events (POST request from WhatsApp).

**Endpoint:** `POST /whatsapp/webhook`

**Request:** WhatsApp webhook payload

**Response:**
```json
{
  "status": "ok"
}
```

#### 6. Get Messages
Get recent message logs.

**Endpoint:** `GET /whatsapp/messages`

**Query Parameters:**
- `limit`: Number of messages (default: 50)

**Response:**
```json
{
  "messages": [
    {
      "timestamp": "2024-01-01T00:00:00",
      "type": "sent_text",
      "data": { ... }
    }
  ],
  "total": 10
}
```

#### 7. Get Configuration
Get WhatsApp configuration status.

**Endpoint:** `GET /whatsapp/config`

**Response:**
```json
{
  "api_token_configured": true,
  "phone_number_id_configured": true,
  "webhook_verify_token": "verify_token_123",
  "webhook_url": "/whatsapp/webhook"
}
```

#### 8. Test Configuration
Test WhatsApp API configuration.

**Endpoint:** `POST /whatsapp/config/test`

**Response:**
```json
{
  "status": "configured",
  "message": "WhatsApp API configuration is valid",
  "details": { ... }
}
```

---

## Common Responses

### Health Check
All services provide a health check endpoint:

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "service-name"
}
```

### Root Endpoint
All services provide service information at root:

**Endpoint:** `GET /`

**Response:**
```json
{
  "service": "Service Name",
  "version": "1.0.0",
  "status": "running"
}
```

---

## Error Responses

All services use standard HTTP status codes:

- `200` - Success
- `400` - Bad Request (invalid input)
- `404` - Not Found
- `500` - Internal Server Error

Error response format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Interactive API Documentation

Each service provides interactive API documentation via Swagger UI:

- OCR Service: http://localhost:8001/docs
- Audio Service: http://localhost:8002/docs
- Agent Creator: http://localhost:8003/docs
- MCP Creator: http://localhost:8004/docs
- WhatsApp Service: http://localhost:8005/docs
