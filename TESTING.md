# Testing Guide

Comprehensive guide for testing all microservices in the platform.

## Prerequisites for Testing

1. All services running via Docker Compose
2. `curl` or Postman for API testing
3. Sample files for testing:
   - PDF document for OCR service
   - Audio file (MP3/WAV) for audio service
   - WhatsApp Business API credentials (for WhatsApp service)

## Quick Start

```bash
# Start all services
docker-compose up -d

# Check all services are healthy
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
curl http://localhost:8005/health
```

## Service-by-Service Testing

### 1. OCR Service Testing

#### Test 1: Extract Text from PDF

```bash
# Create a test PDF first (or use your own)
curl -X POST "http://localhost:8001/ocr/extract" \
  -F "file=@/path/to/your/document.pdf" \
  | jq '.'
```

**Expected Response:**
- Status: 200 OK
- Contains: `file_id`, `filename`, `extraction` with pages and text blocks

#### Test 2: Highlight Search Terms

```bash
curl -X POST "http://localhost:8001/ocr/highlight" \
  -F "file=@/path/to/your/document.pdf" \
  -F "search_terms=important,keyword,example" \
  | jq '.'
```

**Expected Response:**
- Status: 200 OK
- Contains: `file_id`, `highlighted_file`, `download_url`

#### Test 3: Download Highlighted PDF

```bash
# Use the download URL from previous response
curl "http://localhost:8001/ocr/download/{filename}" \
  -o highlighted_output.pdf
```

**Expected Result:**
- Downloaded PDF with yellow highlights on search terms

### 2. Audio Service Testing

#### Test 1: Simple Transcription

```bash
curl -X POST "http://localhost:8002/audio/transcribe" \
  -F "file=@/path/to/your/audio.mp3" \
  | jq '.'
```

**Expected Response:**
- Status: 200 OK
- Contains: `file_id`, `transcription` with text, language, and segments

**Note:** First transcription may take time to download Whisper model.

#### Test 2: Transcription with Highlights

```bash
curl -X POST "http://localhost:8002/audio/highlight" \
  -F "file=@/path/to/your/audio.mp3" \
  -F "keywords=meeting,project,deadline" \
  | jq '.'
```

**Expected Response:**
- Status: 200 OK
- Contains: `transcription` and `highlights` array with keyword matches

#### Test 3: Get Result by ID

```bash
curl "http://localhost:8002/audio/result/{file_id}" \
  | jq '.'
```

### 3. Agent Creator Testing

#### Test 1: List Templates

```bash
curl "http://localhost:8003/agents/templates/list" \
  | jq '.'
```

**Expected Response:**
- List of available templates (customer-support, data-analyst, code-reviewer)

#### Test 2: Create Agent from Template

```bash
curl -X POST "http://localhost:8003/agents/templates/customer-support" \
  | jq '.'
```

**Expected Response:**
- Created agent with `agent_id` and configuration

#### Test 3: Create Custom Agent

```bash
curl -X POST "http://localhost:8003/agents/create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Agent",
    "description": "Test description",
    "system_prompt": "You are a helpful assistant",
    "model": "gpt-4",
    "temperature": 0.7,
    "capabilities": ["text-processing", "analysis"]
  }' \
  | jq '.'
```

**Expected Response:**
- Created agent with unique `agent_id`

#### Test 4: List All Agents

```bash
curl "http://localhost:8003/agents/list" \
  | jq '.'
```

#### Test 5: Get Specific Agent

```bash
curl "http://localhost:8003/agents/{agent_id}" \
  | jq '.'
```

#### Test 6: Update Agent

```bash
curl -X PUT "http://localhost:8003/agents/{agent_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Agent",
    "description": "Updated description",
    "system_prompt": "You are an updated assistant",
    "model": "gpt-4",
    "temperature": 0.8,
    "capabilities": ["updated-capability"]
  }' \
  | jq '.'
```

#### Test 7: Delete Agent

```bash
curl -X DELETE "http://localhost:8003/agents/{agent_id}" \
  | jq '.'
```

### 4. MCP Creator Testing

#### Test 1: Create Simple CRUD API

```bash
curl -X POST "http://localhost:8004/mcp/create" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Todo API",
    "description": "Simple todo management API",
    "base_path": "/api/v1",
    "resources": [
      {
        "name": "todo",
        "description": "Todo item",
        "fields": [
          {
            "name": "title",
            "type": "string",
            "required": true,
            "description": "Todo title"
          },
          {
            "name": "completed",
            "type": "boolean",
            "required": true,
            "description": "Completion status"
          },
          {
            "name": "priority",
            "type": "integer",
            "required": false,
            "description": "Priority level"
          }
        ],
        "enable_create": true,
        "enable_read": true,
        "enable_update": true,
        "enable_delete": true,
        "enable_list": true
      }
    ]
  }' \
  | jq '.'
```

**Expected Response:**
- Created project with `project_id`
- List of generated files
- Complete API code in response

#### Test 2: Create Multi-Resource API

```bash
curl -X POST "http://localhost:8004/mcp/create" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Blog API",
    "description": "Blog management system",
    "base_path": "/api/v1",
    "resources": [
      {
        "name": "post",
        "description": "Blog post",
        "fields": [
          {"name": "title", "type": "string", "required": true},
          {"name": "content", "type": "string", "required": true},
          {"name": "published", "type": "boolean", "required": true}
        ],
        "enable_create": true,
        "enable_read": true,
        "enable_update": true,
        "enable_delete": true,
        "enable_list": true
      },
      {
        "name": "comment",
        "description": "Blog comment",
        "fields": [
          {"name": "post_id", "type": "string", "required": true},
          {"name": "author", "type": "string", "required": true},
          {"name": "text", "type": "string", "required": true}
        ],
        "enable_create": true,
        "enable_read": true,
        "enable_update": false,
        "enable_delete": true,
        "enable_list": true
      }
    ]
  }' \
  | jq '.'
```

#### Test 3: List Projects

```bash
curl "http://localhost:8004/mcp/list" \
  | jq '.'
```

#### Test 4: Get Project Code

```bash
curl "http://localhost:8004/mcp/code/{project_id}" \
  | jq -r '.code'
```

#### Test 5: Get Full Project Details

```bash
curl "http://localhost:8004/mcp/{project_id}" \
  | jq '.'
```

### 5. WhatsApp Service Testing

**Note:** WhatsApp service requires valid API credentials. Set these in `.env` file first.

#### Test 1: Check Configuration

```bash
curl "http://localhost:8005/whatsapp/config" \
  | jq '.'
```

**Expected Response:**
- Configuration status for token and phone number

#### Test 2: Test Configuration

```bash
curl -X POST "http://localhost:8005/whatsapp/config/test" \
  | jq '.'
```

#### Test 3: Send Text Message

```bash
curl -X POST "http://localhost:8005/whatsapp/send/text" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+1234567890",
    "message": "Test message from microservices platform"
  }' \
  | jq '.'
```

**Note:** Replace phone number with valid WhatsApp number (with country code)

#### Test 4: Send Template Message

```bash
curl -X POST "http://localhost:8005/whatsapp/send/template" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+1234567890",
    "template_name": "hello_world",
    "language_code": "en"
  }' \
  | jq '.'
```

#### Test 5: Send Media Message

```bash
curl -X POST "http://localhost:8005/whatsapp/send/media" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+1234567890",
    "media_type": "image",
    "media_url": "https://example.com/image.jpg",
    "caption": "Test image"
  }' \
  | jq '.'
```

#### Test 6: View Message Logs

```bash
curl "http://localhost:8005/whatsapp/messages?limit=10" \
  | jq '.'
```

## Frontend UI Testing

### Access the UI

Navigate to: http://localhost:3000

### Test Each Service Page

1. **Home Page**
   - Verify all service cards are displayed
   - Click each card to navigate to service page

2. **OCR Service Page**
   - Upload a PDF file
   - Test "Extract Text" mode
   - Test "Highlight" mode with search terms
   - Verify results display correctly
   - Download highlighted PDF

3. **Audio Service Page**
   - Upload an audio file (MP3/WAV)
   - Test "Transcribe Audio" mode
   - Test "Transcribe with Highlights" mode
   - Verify transcription displays
   - Check highlights are shown correctly

4. **Agent Creator Page**
   - View available templates
   - Create agent from template
   - Create custom agent with form
   - View created agents list
   - Verify agent details

5. **MCP Creator Page**
   - Create a simple CRUD API
   - Add multiple resources
   - Add fields to resources
   - View generated code
   - List created projects

6. **WhatsApp Service Page**
   - Check configuration status
   - Test text message sending
   - Test template message sending
   - Test media message sending
   - View message logs

## Automated Testing with Scripts

### Test All Services

```bash
#!/bin/bash

echo "Testing all microservices..."

# Test health endpoints
for port in 8001 8002 8003 8004 8005; do
  echo "Testing service on port $port..."
  curl -s "http://localhost:$port/health" | jq '.'
done

# Test OCR service
echo "Testing OCR service..."
curl -s "http://localhost:8001/" | jq '.'

# Test Audio service
echo "Testing Audio service..."
curl -s "http://localhost:8002/" | jq '.'

# Test Agent Creator
echo "Testing Agent Creator..."
curl -s "http://localhost:8003/agents/templates/list" | jq '.'

# Test MCP Creator
echo "Testing MCP Creator..."
curl -s "http://localhost:8004/mcp/list" | jq '.'

# Test WhatsApp service
echo "Testing WhatsApp service..."
curl -s "http://localhost:8005/whatsapp/config" | jq '.'

echo "All tests completed!"
```

## Performance Testing

### Load Testing with Apache Bench

```bash
# Test OCR service health endpoint
ab -n 1000 -c 10 http://localhost:8001/health

# Test Agent Creator list endpoint
ab -n 1000 -c 10 http://localhost:8003/agents/list
```

### Response Time Benchmarks

Expected response times (local environment):

- Health checks: < 50ms
- Agent creation: < 200ms
- OCR extraction: 2-10s (depends on PDF size)
- Audio transcription: 10-60s (depends on audio length)
- MCP code generation: < 500ms
- WhatsApp message send: 1-3s

## Troubleshooting Tests

### Service Not Responding

```bash
# Check if service is running
docker-compose ps

# Check service logs
docker-compose logs [service-name]

# Restart specific service
docker-compose restart [service-name]
```

### Connection Refused

```bash
# Check if ports are in use
netstat -an | grep LISTEN | grep -E '3000|8001|8002|8003|8004|8005'

# Verify services are healthy
docker-compose ps
```

### File Upload Fails

```bash
# Check upload directory permissions
ls -la uploads/

# Verify file size limits
# Check Docker volume mounts in docker-compose.yml
```

### WhatsApp Tests Fail

1. Verify API token is set correctly in `.env`
2. Check WhatsApp Business API account is active
3. Verify phone number format includes country code
4. Check webhook configuration if receiving messages

## CI/CD Testing

### GitHub Actions Example

```yaml
name: Test Microservices

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build services
        run: docker-compose build
      
      - name: Start services
        run: docker-compose up -d
      
      - name: Wait for services
        run: sleep 30
      
      - name: Test health endpoints
        run: |
          curl -f http://localhost:8001/health
          curl -f http://localhost:8002/health
          curl -f http://localhost:8003/health
          curl -f http://localhost:8004/health
          curl -f http://localhost:8005/health
      
      - name: Shutdown services
        run: docker-compose down
```

## Test Coverage Goals

- API endpoint coverage: 100%
- Service health checks: 100%
- Error handling: 80%+
- Frontend component rendering: 90%+

## Reporting Issues

When reporting test failures, include:

1. Service name and version
2. Endpoint being tested
3. Request payload
4. Expected vs actual response
5. Docker logs: `docker-compose logs [service]`
6. Environment details (OS, Docker version)
