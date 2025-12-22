# AI-First Microservices Platform

A comprehensive microservices architecture designed for AI-first applications, featuring specialized services for OCR, audio transcription, agent creation, API generation, and WhatsApp integration.

## 🚀 Features

### 1. OCR Service
- Extract text from PDF documents with precise coordinates
- Highlight specific search terms in PDFs
- Visual context preservation
- Support for multi-page documents

### 2. Audio Transcription Service
- Transcribe audio files using OpenAI Whisper
- Generate timestamps for each segment
- Highlight specific keywords with context
- Support for multiple audio formats (MP3, WAV, M4A, OGG, FLAC)

### 3. Agent Creator
- Create and manage AI agents
- Configure system prompts, models, and capabilities
- Pre-built templates for common use cases
- Export agent configurations

### 4. MCP Creator (Model Context Protocol)
- Generate complete CRUD APIs automatically
- Define resources and fields visually
- Get production-ready FastAPI code
- Docker support included

### 5. WhatsApp Integration
- Send text, template, and media messages
- Webhook support for receiving messages
- Message logging and tracking
- WhatsApp Business API integration

### 6. Modern Web UI
- Clean, intuitive interface
- Responsive design
- Real-time feedback
- File upload and download support

## 📋 Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local service development)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/shashanksaxena-tz/Microservices.git
cd Microservices
```

2. Copy the environment file and configure:
```bash
cp .env.example .env
```

3. Edit `.env` file with your WhatsApp API credentials (optional):
```
WHATSAPP_API_TOKEN=your_token_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_id_here
WEBHOOK_VERIFY_TOKEN=your_verify_token_here
```

4. Build and start all services:
```bash
docker-compose up --build
```

## 🌐 Service Endpoints

Once running, the services are available at:

- **Frontend UI**: http://localhost:3000
- **OCR Service**: http://localhost:8001
  - API Docs: http://localhost:8001/docs
- **Audio Service**: http://localhost:8002
  - API Docs: http://localhost:8002/docs
- **Agent Creator**: http://localhost:8003
  - API Docs: http://localhost:8003/docs
- **MCP Creator**: http://localhost:8004
  - API Docs: http://localhost:8004/docs
- **WhatsApp Service**: http://localhost:8005
  - API Docs: http://localhost:8005/docs

## 📖 Usage Guide

### OCR Service

**Extract Text from PDF:**
```bash
curl -X POST "http://localhost:8001/ocr/extract" \
  -F "file=@document.pdf"
```

**Highlight Search Terms:**
```bash
curl -X POST "http://localhost:8001/ocr/highlight" \
  -F "file=@document.pdf" \
  -F "search_terms=important,keyword,terms"
```

### Audio Transcription Service

**Transcribe Audio:**
```bash
curl -X POST "http://localhost:8002/audio/transcribe" \
  -F "file=@audio.mp3"
```

**Transcribe with Highlights:**
```bash
curl -X POST "http://localhost:8002/audio/highlight" \
  -F "file=@audio.mp3" \
  -F "keywords=meeting,action,deadline"
```

### Agent Creator

**Create an Agent:**
```bash
curl -X POST "http://localhost:8003/agents/create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Support Agent",
    "description": "Handles customer queries",
    "system_prompt": "You are a helpful support agent",
    "model": "gpt-4",
    "temperature": 0.7,
    "capabilities": ["text-understanding", "response-generation"]
  }'
```

### MCP Creator

**Generate CRUD API:**
```bash
curl -X POST "http://localhost:8004/mcp/create" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "User Management API",
    "description": "API for managing users",
    "base_path": "/api/v1",
    "resources": [
      {
        "name": "user",
        "description": "User resource",
        "fields": [
          {"name": "name", "type": "string", "required": true},
          {"name": "email", "type": "string", "required": true},
          {"name": "age", "type": "integer", "required": false}
        ]
      }
    ]
  }'
```

### WhatsApp Service

**Send Text Message:**
```bash
curl -X POST "http://localhost:8005/whatsapp/send/text" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+1234567890",
    "message": "Hello from the microservices platform!"
  }'
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│                      Port: 3000                              │
└─────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
    ┌────▼────┐          ┌────▼────┐          ┌───▼─────┐
    │   OCR   │          │  Audio  │          │  Agent  │
    │ Service │          │ Service │          │ Creator │
    │  :8001  │          │  :8002  │          │  :8003  │
    └─────────┘          └─────────┘          └─────────┘
         │                                          │
         └────────────────┬─────────────────────────┘
                          │
                     ┌────▼────┐          ┌──────────┐
                     │   MCP   │          │ WhatsApp │
                     │ Creator │          │ Service  │
                     │  :8004  │          │  :8005   │
                     └─────────┘          └──────────┘
```

## 🔧 Development

### Running Individual Services

**OCR Service:**
```bash
cd services/ocr-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

**Audio Service:**
```bash
cd services/audio-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

### Adding New Services

1. Create a new directory in `services/`
2. Add Dockerfile and requirements.txt
3. Create main.py with FastAPI application
4. Add service to docker-compose.yml
5. Create corresponding UI component in frontend

## 📦 Project Structure

```
Microservices/
├── services/
│   ├── ocr-service/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── main.py
│   ├── audio-service/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── main.py
│   ├── agent-creator/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── main.py
│   ├── mcp-creator/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── main.py
│   └── whatsapp-service/
│       ├── Dockerfile
│       ├── requirements.txt
│       └── main.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.js
│   │   └── index.js
│   ├── Dockerfile
│   └── package.json
├── uploads/
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## 🔒 Security Notes

- WhatsApp API credentials should be kept secure
- Use environment variables for sensitive data
- In production, implement proper authentication
- Enable HTTPS for all services
- Validate and sanitize all user inputs

## 🐛 Troubleshooting

**Services not starting:**
- Check Docker is running
- Ensure ports 3000, 8001-8005 are available
- Review logs: `docker-compose logs [service-name]`

**WhatsApp not working:**
- Verify API credentials in .env file
- Check WhatsApp Business API account status
- Review webhook configuration

**OCR/Audio processing slow:**
- These services are compute-intensive
- Consider increasing Docker resources
- Use smaller files for testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- OpenAI Whisper for audio transcription
- PyMuPDF for PDF processing
- React for the frontend framework
- WhatsApp Business API for messaging integration

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: shashanksaxena-tz

---

Built with ❤️ for AI-First Applications
