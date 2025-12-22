# Quick Reference Guide

## 🚀 Quick Start

```bash
# Clone and start
git clone https://github.com/shashanksaxena-tz/Microservices.git
cd Microservices
cp .env.example .env
./setup.sh
```

## 📊 Service Overview

| Service | Port | Purpose | Key Features |
|---------|------|---------|--------------|
| Frontend | 3000 | Web UI | React-based dashboard |
| OCR | 8001 | PDF Processing | Text extraction, highlighting |
| Audio | 8002 | Transcription | Speech-to-text, highlights |
| Agent Creator | 8003 | AI Agents | Agent management, templates |
| MCP Creator | 8004 | API Generator | CRUD API generation |
| WhatsApp | 8005 | Messaging | WhatsApp Business API |

## 🔗 Quick Access

- **UI Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:800[1-5]/docs

## 💻 Common Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f [service-name]

# Restart service
docker-compose restart [service-name]

# Stop all services
docker-compose down

# Rebuild after changes
docker-compose up --build
```

## 📝 Quick Examples

### OCR - Extract Text
```bash
curl -X POST http://localhost:8001/ocr/extract \
  -F "file=@document.pdf"
```

### Audio - Transcribe
```bash
curl -X POST http://localhost:8002/audio/transcribe \
  -F "file=@audio.mp3"
```

### Agent - Create
```bash
curl -X POST http://localhost:8003/agents/create \
  -H "Content-Type: application/json" \
  -d '{"name":"Bot","description":"Helper","system_prompt":"You help users","model":"gpt-4","temperature":0.7}'
```

### MCP - Generate API
```bash
curl -X POST http://localhost:8004/mcp/create \
  -H "Content-Type: application/json" \
  -d '{"project_name":"User API","description":"User management","base_path":"/api/v1","resources":[{"name":"user","description":"User","fields":[{"name":"name","type":"string","required":true}]}]}'
```

### WhatsApp - Send Message
```bash
curl -X POST http://localhost:8005/whatsapp/send/text \
  -H "Content-Type: application/json" \
  -d '{"to":"+1234567890","message":"Hello!"}'
```

## 🔧 Service Health Checks

```bash
# Check all services
for port in 8001 8002 8003 8004 8005; do
  curl http://localhost:$port/health
done
```

## 🎯 Key Files

- `docker-compose.yml` - Service orchestration
- `.env` - Environment configuration
- `README.md` - Full documentation
- `API_DOCS.md` - API reference
- `TESTING.md` - Testing guide
- `setup.sh` - Setup automation

## 🛠️ Development

```bash
# Run single service locally
cd services/ocr-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8001

# Run frontend locally
cd frontend
npm install
npm start
```

## 📦 File Structure

```
Microservices/
├── services/          # Backend microservices
│   ├── ocr-service/
│   ├── audio-service/
│   ├── agent-creator/
│   ├── mcp-creator/
│   └── whatsapp-service/
├── frontend/          # React UI
├── uploads/           # File storage
└── docker-compose.yml # Container orchestration
```

## 🔐 Environment Variables

Edit `.env` for WhatsApp integration:

```env
WHATSAPP_API_TOKEN=your_token
WHATSAPP_PHONE_NUMBER_ID=your_id
WEBHOOK_VERIFY_TOKEN=your_verify_token
```

## 🐛 Common Issues

**Services won't start:**
- Check Docker is running
- Verify ports 3000, 8001-8005 are free
- Run: `docker-compose down && docker-compose up -d`

**File uploads fail:**
- Check `uploads/` directory exists
- Verify Docker volume mounts

**WhatsApp not working:**
- Configure credentials in `.env`
- Test: `curl http://localhost:8005/whatsapp/config/test`

## 📈 Performance Tips

- OCR: Use smaller PDFs for faster processing
- Audio: Whisper model downloads on first use (~150MB)
- Production: Use external storage for uploads
- Scale: Increase Docker resources for better performance

## 🎓 Learning Resources

- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- Docker: https://docs.docker.com/
- WhatsApp API: https://developers.facebook.com/docs/whatsapp

## 📞 Support

- GitHub Issues: Report bugs
- Documentation: README.md, API_DOCS.md
- Examples: TESTING.md

## ⚡ Pro Tips

1. Use interactive API docs at `/docs` endpoints
2. Check service logs for debugging
3. Test with small files first
4. Keep Docker images updated
5. Monitor resource usage with `docker stats`

---

**Built for AI-First Applications** 🤖
