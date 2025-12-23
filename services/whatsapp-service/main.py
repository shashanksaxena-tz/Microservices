from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import httpx
import os
from datetime import datetime
import json
from pathlib import Path

app = FastAPI(title="WhatsApp Integration Service", description="WhatsApp Business API integration")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WhatsApp API configuration
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN", "")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "verify_token_123")
WHATSAPP_API_URL = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

# Storage for messages
MESSAGES_DIR = Path(os.getenv("UPLOAD_DIR", "/uploads")) / "whatsapp"
MESSAGES_DIR.mkdir(parents=True, exist_ok=True)

messages_log: List[Dict] = []


class TextMessage(BaseModel):
    to: str = Field(..., description="Recipient phone number (with country code)")
    message: str = Field(..., description="Message text to send")


class TemplateMessage(BaseModel):
    to: str = Field(..., description="Recipient phone number (with country code)")
    template_name: str = Field(..., description="Template name")
    language_code: str = Field(default="en", description="Language code")


class MediaMessage(BaseModel):
    to: str = Field(..., description="Recipient phone number (with country code)")
    media_type: str = Field(..., description="Type: image, video, audio, document")
    media_url: str = Field(..., description="URL of the media file")
    caption: Optional[str] = Field(None, description="Optional caption")


async def send_whatsapp_message(payload: Dict) -> Dict:
    """Send message via WhatsApp Business API."""
    if not WHATSAPP_API_TOKEN:
        raise HTTPException(
            status_code=500,
            detail="WhatsApp API token not configured. Set WHATSAPP_API_TOKEN environment variable."
        )
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                WHATSAPP_API_URL,
                headers=headers,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=500,
                detail=f"WhatsApp API error: {str(e)}"
            )


def log_message(message_type: str, data: Dict):
    """Log sent/received messages."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "type": message_type,
        "data": data
    }
    messages_log.append(log_entry)
    
    # Save to file
    log_file = MESSAGES_DIR / "messages.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


@app.get("/")
async def root():
    return {
        "service": "WhatsApp Integration Service",
        "version": "1.0.0",
        "status": "running",
        "configured": bool(WHATSAPP_API_TOKEN)
    }


@app.post("/whatsapp/send/text")
async def send_text_message(message: TextMessage):
    """Send a text message via WhatsApp."""
    payload = {
        "messaging_product": "whatsapp",
        "to": message.to,
        "type": "text",
        "text": {
            "body": message.message
        }
    }
    
    result = await send_whatsapp_message(payload)
    
    # Log the message
    log_message("sent_text", {
        "to": message.to,
        "message": message.message,
        "response": result
    })
    
    return {
        "status": "sent",
        "to": message.to,
        "message": message.message,
        "response": result
    }


@app.post("/whatsapp/send/template")
async def send_template_message(message: TemplateMessage):
    """Send a template message via WhatsApp."""
    payload = {
        "messaging_product": "whatsapp",
        "to": message.to,
        "type": "template",
        "template": {
            "name": message.template_name,
            "language": {
                "code": message.language_code
            }
        }
    }
    
    result = await send_whatsapp_message(payload)
    
    # Log the message
    log_message("sent_template", {
        "to": message.to,
        "template": message.template_name,
        "response": result
    })
    
    return {
        "status": "sent",
        "to": message.to,
        "template": message.template_name,
        "response": result
    }


@app.post("/whatsapp/send/media")
async def send_media_message(message: MediaMessage):
    """Send a media message via WhatsApp."""
    media_object = {
        "link": message.media_url
    }
    
    if message.caption:
        media_object["caption"] = message.caption
    
    payload = {
        "messaging_product": "whatsapp",
        "to": message.to,
        "type": message.media_type,
        message.media_type: media_object
    }
    
    result = await send_whatsapp_message(payload)
    
    # Log the message
    log_message("sent_media", {
        "to": message.to,
        "media_type": message.media_type,
        "media_url": message.media_url,
        "response": result
    })
    
    return {
        "status": "sent",
        "to": message.to,
        "media_type": message.media_type,
        "response": result
    }


@app.get("/whatsapp/webhook")
async def webhook_verify(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    """Verify WhatsApp webhook."""
    if hub_mode == "subscribe" and hub_verify_token == WEBHOOK_VERIFY_TOKEN:
        return int(hub_challenge)
    
    raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/whatsapp/webhook")
async def webhook_receive(request: Request):
    """Receive WhatsApp webhook events."""
    try:
        body = await request.json()
        
        # Log received webhook
        log_message("webhook_received", body)
        
        # Process webhook data
        if body.get("object") == "whatsapp_business_account":
            for entry in body.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    
                    # Process messages
                    if "messages" in value:
                        for message in value["messages"]:
                            log_message("received_message", message)
                    
                    # Process statuses
                    if "statuses" in value:
                        for status in value["statuses"]:
                            log_message("message_status", status)
        
        return {"status": "ok"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook processing error: {str(e)}")


@app.get("/whatsapp/messages")
async def get_messages(limit: int = 50):
    """Get recent message logs."""
    return {
        "messages": messages_log[-limit:],
        "total": len(messages_log)
    }


@app.get("/whatsapp/config")
async def get_config():
    """Get WhatsApp configuration status."""
    return {
        "api_token_configured": bool(WHATSAPP_API_TOKEN),
        "phone_number_id_configured": bool(WHATSAPP_PHONE_NUMBER_ID),
        "webhook_verify_token": WEBHOOK_VERIFY_TOKEN,
        "webhook_url": "/whatsapp/webhook"
    }


@app.post("/whatsapp/config/test")
async def test_configuration():
    """Test WhatsApp API configuration."""
    if not WHATSAPP_API_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
        return {
            "status": "not_configured",
            "message": "Please set WHATSAPP_API_TOKEN and WHATSAPP_PHONE_NUMBER_ID environment variables"
        }
    
    # Try to make a test API call
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}",
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            return {
                "status": "configured",
                "message": "WhatsApp API configuration is valid",
                "details": response.json()
            }
        except httpx.HTTPError as e:
            return {
                "status": "error",
                "message": f"Configuration test failed: {str(e)}"
            }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "whatsapp-service"}
