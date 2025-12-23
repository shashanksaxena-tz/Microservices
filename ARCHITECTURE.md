# Architecture Documentation

## System Architecture

### Overview

The AI-First Microservices Platform is a distributed system built on a microservices architecture pattern, designed for scalability, maintainability, and independent service deployment.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Client Layer                                 │
│                      (Web Browsers, Mobile)                          │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Frontend Service                              │
│                     React Application (Port 3000)                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Components:                                                   │  │
│  │  • Home Dashboard                                             │  │
│  │  • OCR Interface                                              │  │
│  │  • Audio Interface                                            │  │
│  │  • Agent Creator UI                                           │  │
│  │  • MCP Creator UI                                             │  │
│  │  • WhatsApp Interface                                         │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ REST API
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                               │
│                   (Load Balancing, Routing)                          │
└──┬────────┬────────┬────────┬────────┬────────────────────────────┬─┘
   │        │        │        │        │                            │
   ▼        ▼        ▼        ▼        ▼                            ▼
┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐              ┌──────────────┐
│ OCR │  │Audio│  │Agent│  │ MCP │  │WhatsA│              │   External   │
│Service  │Service │Creator  │Creator │pp Svc│              │   Services   │
│:8001│  │:8002│  │:8003│  │:8004│  │:8005│              └──────────────┘
└─────┘  └─────┘  └─────┘  └─────┘  └─────┘                      │
   │        │        │        │        │                            │
   │        │        │        │        └────────────────────────────┤
   │        │        │        │                                     │
   │        │        │        │                          ┌──────────▼──────┐
   │        │        │        │                          │  WhatsApp API   │
   │        │        │        │                          │  (Facebook)     │
   │        │        │        │                          └─────────────────┘
   │        │        │        │
   ▼        ▼        ▼        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Storage Layer                                 │
│  ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │   OCR    │  │   Audio   │  │  Agent   │  │   MCP Projects   │  │
│  │  Files   │  │   Files   │  │  Configs │  │   Generated Code │  │
│  │ /uploads │  │ /uploads  │  │ /uploads │  │    /uploads      │  │
│  └──────────┘  └───────────┘  └──────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Service Architecture

### 1. OCR Service (Port 8001)

```
┌─────────────────────────────────────┐
│         OCR Service                  │
├─────────────────────────────────────┤
│ Technology Stack:                    │
│ • FastAPI (Web Framework)            │
│ • PyMuPDF (PDF Processing)          │
│ • Tesseract (OCR Engine)            │
│ • pdf2image (PDF Conversion)        │
├─────────────────────────────────────┤
│ API Endpoints:                       │
│ POST /ocr/extract                    │
│ POST /ocr/highlight                  │
│ GET  /ocr/download/{filename}        │
├─────────────────────────────────────┤
│ Features:                            │
│ • Text extraction with coordinates   │
│ • PDF highlighting                   │
│ • Multi-page support                 │
└─────────────────────────────────────┘
```

### 2. Audio Service (Port 8002)

```
┌─────────────────────────────────────┐
│      Audio Transcription Service    │
├─────────────────────────────────────┤
│ Technology Stack:                    │
│ • FastAPI (Web Framework)            │
│ • OpenAI Whisper (Transcription)    │
│ • pydub (Audio Processing)          │
├─────────────────────────────────────┤
│ API Endpoints:                       │
│ POST /audio/transcribe               │
│ POST /audio/highlight                │
│ GET  /audio/result/{file_id}         │
├─────────────────────────────────────┤
│ Features:                            │
│ • Speech-to-text conversion          │
│ • Timestamp generation               │
│ • Keyword highlighting               │
│ • Multiple format support            │
└─────────────────────────────────────┘
```

### 3. Agent Creator Service (Port 8003)

```
┌─────────────────────────────────────┐
│       Agent Creator Service          │
├─────────────────────────────────────┤
│ Technology Stack:                    │
│ • FastAPI (Web Framework)            │
│ • Pydantic (Data Validation)        │
│ • Jinja2 (Templating)               │
├─────────────────────────────────────┤
│ API Endpoints:                       │
│ POST   /agents/create                │
│ GET    /agents/list                  │
│ GET    /agents/{id}                  │
│ PUT    /agents/{id}                  │
│ DELETE /agents/{id}                  │
│ GET    /agents/templates/list        │
│ POST   /agents/templates/{id}        │
├─────────────────────────────────────┤
│ Features:                            │
│ • Agent configuration management     │
│ • Template system                    │
│ • JSON/YAML export                   │
└─────────────────────────────────────┘
```

### 4. MCP Creator Service (Port 8004)

```
┌─────────────────────────────────────┐
│        MCP Creator Service           │
├─────────────────────────────────────┤
│ Technology Stack:                    │
│ • FastAPI (Web Framework)            │
│ • Jinja2 (Code Generation)          │
│ • SQLAlchemy (ORM Support)          │
├─────────────────────────────────────┤
│ API Endpoints:                       │
│ POST   /mcp/create                   │
│ GET    /mcp/list                     │
│ GET    /mcp/{project_id}             │
│ GET    /mcp/code/{project_id}        │
│ DELETE /mcp/{project_id}             │
├─────────────────────────────────────┤
│ Features:                            │
│ • CRUD API generation                │
│ • Multi-resource support             │
│ • FastAPI code generation            │
│ • Docker configuration               │
└─────────────────────────────────────┘
```

### 5. WhatsApp Service (Port 8005)

```
┌─────────────────────────────────────┐
│     WhatsApp Integration Service     │
├─────────────────────────────────────┤
│ Technology Stack:                    │
│ • FastAPI (Web Framework)            │
│ • httpx (HTTP Client)               │
│ • WhatsApp Business API             │
├─────────────────────────────────────┤
│ API Endpoints:                       │
│ POST /whatsapp/send/text             │
│ POST /whatsapp/send/template         │
│ POST /whatsapp/send/media            │
│ GET  /whatsapp/webhook               │
│ POST /whatsapp/webhook               │
│ GET  /whatsapp/messages              │
│ GET  /whatsapp/config                │
│ POST /whatsapp/config/test           │
├─────────────────────────────────────┤
│ Features:                            │
│ • Text/media message sending         │
│ • Webhook integration                │
│ • Message logging                    │
│ • Template messages                  │
└─────────────────────────────────────┘
```

### 6. API Gateway Service (Port 8000)

```
┌─────────────────────────────────────┐
│         API Gateway Service          │
├─────────────────────────────────────┤
│ Technology Stack:                    │
│ • FastAPI (Web Framework)            │
│ • httpx (Async HTTP Client)          │
├─────────────────────────────────────┤
│ API Endpoints:                       │
│ /api/ocr/* → OCR Service             │
│ /api/audio/* → Audio Service         │
│ /api/agent/* → Agent Creator         │
│ /api/mcp/* → MCP Creator             │
│ /api/whatsapp/* → WhatsApp Service   │
├─────────────────────────────────────┤
│ Features:                            │
│ • Unified entry point                │
│ • API Key Authentication             │
│ • Request Logging                    │
│ • Health Checks                      │
└─────────────────────────────────────┘
```

### 7. Frontend Service (Port 3000)

```
┌─────────────────────────────────────┐
│        Frontend Application          │
├─────────────────────────────────────┤
│ Technology Stack:                    │
│ • React 18                           │
│ • React Router                       │
│ • Axios (HTTP Client)               │
├─────────────────────────────────────┤
│ Pages:                               │
│ • Home Dashboard                     │
│ • OCR Service Interface              │
│ • Audio Service Interface            │
│ • Agent Creator Interface            │
│ • MCP Creator Interface              │
│ • WhatsApp Service Interface         │
├─────────────────────────────────────┤
│ Features:                            │
│ • Responsive design                  │
│ • File upload/download               │
│ • Real-time feedback                 │
│ • Service integration                │
└─────────────────────────────────────┘
```

## Data Flow

### OCR Processing Flow

```
User → Upload PDF → Frontend → OCR Service
                                    ↓
                         Extract Text with Coordinates
                                    ↓
                         Store in /uploads/ocr/
                                    ↓
                         Return Results → Frontend → User
```

### Audio Transcription Flow

```
User → Upload Audio → Frontend → Audio Service
                                      ↓
                         Load Whisper Model (first time)
                                      ↓
                         Transcribe with Timestamps
                                      ↓
                         Generate Highlights (if keywords)
                                      ↓
                         Store in /uploads/audio/
                                      ↓
                         Return Results → Frontend → User
```

### Agent Creation Flow

```
User → Configure Agent → Frontend → Agent Creator
                                         ↓
                         Validate Configuration
                                         ↓
                         Generate Agent Config
                                         ↓
                         Store JSON/YAML in /uploads/agents/
                                         ↓
                         Return Agent ID → Frontend → User
```

### MCP API Generation Flow

```
User → Define Resources → Frontend → MCP Creator
                                         ↓
                         Validate Resource Schema
                                         ↓
                         Generate FastAPI Code
                                         ↓
                         Generate Docker Files
                                         ↓
                         Store in /uploads/mcp/{project_id}/
                                         ↓
                         Return Generated Code → Frontend → User
```

### WhatsApp Message Flow

```
User → Compose Message → Frontend → WhatsApp Service
                                         ↓
                         Validate Configuration
                                         ↓
                         Call WhatsApp Business API
                                         ↓
                         Log Message
                                         ↓
                         Return Status → Frontend → User

WhatsApp → Webhook → WhatsApp Service
                          ↓
                     Process Event
                          ↓
                     Log Message
                          ↓
                     Return 200 OK
```

## Deployment Architecture

### Docker Compose Structure

```
┌──────────────────────────────────────────────────────┐
│              Docker Host Machine                      │
│                                                       │
│  ┌────────────────────────────────────────────────┐ │
│  │         Docker Network (bridge)                 │ │
│  │                                                 │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐    │ │
│  │  │ Frontend │  │   OCR    │  │  Audio   │    │ │
│  │  │Container │  │Container │  │Container │    │ │
│  │  └──────────┘  └──────────┘  └──────────┘    │ │
│  │                                                │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐    │ │
│  │  │  Agent   │  │   MCP    │  │ WhatsApp │    │ │
│  │  │Container │  │Container │  │Container │    │ │
│  │  └──────────┘  └──────────┘  └──────────┘    │ │
│  │                                                │ │
│  └────────────────────────────────────────────────┘ │
│                                                      │
│  ┌────────────────────────────────────────────────┐ │
│  │         Shared Volume: /uploads                 │ │
│  │  • ocr/      • audio/    • agents/             │ │
│  │  • mcp/      • whatsapp/                       │ │
│  └────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

## Technology Stack Summary

### Backend Services
- **Framework**: FastAPI (Python 3.11)
- **API Documentation**: OpenAPI/Swagger
- **CORS**: Enabled for all origins
- **Containerization**: Docker

### Frontend
- **Framework**: React 18
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Styling**: Custom CSS

### Storage
- **File Storage**: Local filesystem (Docker volumes)
- **Configuration**: Environment variables (.env)

### External Services
- **WhatsApp Business API**: Meta/Facebook platform
- **AI Models**: OpenAI Whisper (local)

## Security Considerations

1. **CORS**: Currently allows all origins (development mode)
2. **Authentication**: Not implemented (add for production)
3. **File Upload**: No size limits enforced (add for production)
4. **API Keys**: Stored in environment variables
5. **HTTPS**: Not configured (add for production)

## Scalability

### Horizontal Scaling
- Each service can be scaled independently
- Load balancer needed for multiple instances
- Shared storage should be migrated to cloud (S3, Azure Blob)

### Vertical Scaling
- Increase Docker resource allocation
- Optimize AI model loading
- Add caching layer (Redis)

### Performance Optimization
- Add message queue (RabbitMQ, Kafka)
- Implement result caching
- Use CDN for frontend
- Add database for persistent storage

## Monitoring & Logging

### Current State
- Docker logs available via `docker-compose logs`
- Console logging in services
- No centralized monitoring

### Production Recommendations
- Add Prometheus for metrics
- Use ELK stack for log aggregation
- Implement health check endpoints (✓ already available)
- Add APM (Application Performance Monitoring)

## Future Enhancements

1. **Authentication & Authorization**
   - JWT-based authentication
   - Role-based access control
   - API key management

2. **Database Integration**
   - PostgreSQL for persistent storage
   - Redis for caching
   - MongoDB for document storage

3. **Message Queue**
   - Asynchronous processing
   - Job queuing for heavy operations
   - Event-driven architecture

4. **Cloud Deployment**
   - Kubernetes orchestration
   - Cloud storage integration
   - Auto-scaling policies

5. **Enhanced Features**
   - Batch processing
   - Real-time notifications
   - Advanced analytics
   - Multi-language support

---

**Architecture Version**: 1.0.0  
**Last Updated**: 2024  
**Maintained By**: Development Team
