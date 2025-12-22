#!/bin/bash

# Setup script for Microservices Platform
echo "🚀 Setting up AI-First Microservices Platform..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✓ Docker and Docker Compose are installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created. Please edit it with your WhatsApp API credentials if needed."
fi

# Create uploads directory structure
echo "📁 Creating upload directories..."
mkdir -p uploads/ocr uploads/audio uploads/agents uploads/mcp uploads/whatsapp

echo "✓ Upload directories created"

# Build and start services
echo "🏗️  Building and starting services..."
docker-compose up --build -d

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Service URLs:"
echo "   Frontend:        http://localhost:3000"
echo "   OCR Service:     http://localhost:8001"
echo "   Audio Service:   http://localhost:8002"
echo "   Agent Creator:   http://localhost:8003"
echo "   MCP Creator:     http://localhost:8004"
echo "   WhatsApp Service: http://localhost:8005"
echo ""
echo "📖 View API documentation at:"
echo "   http://localhost:8001/docs (OCR)"
echo "   http://localhost:8002/docs (Audio)"
echo "   http://localhost:8003/docs (Agent Creator)"
echo "   http://localhost:8004/docs (MCP Creator)"
echo "   http://localhost:8005/docs (WhatsApp)"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop services: docker-compose down"
