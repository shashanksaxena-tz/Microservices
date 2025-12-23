from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import whisper
import os
import json
from pathlib import Path
from typing import List, Dict, Optional
import uuid
from pydub import AudioSegment
import os

app = FastAPI(title="Audio Transcription Service", description="Audio transcription with highlight generation")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/uploads")) / "audio"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Load Whisper model (using base model for balance of speed and accuracy)
model = None


def get_model():
    """Lazy load the Whisper model."""
    global model
    if model is None:
        model = whisper.load_model("base")
    return model


def transcribe_audio(audio_path: str) -> Dict:
    """Transcribe audio file with timestamps."""
    model = get_model()
    result = model.transcribe(audio_path, word_timestamps=True)
    
    return {
        "text": result["text"],
        "language": result["language"],
        "segments": [
            {
                "id": segment["id"],
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"],
                "words": segment.get("words", [])
            }
            for segment in result["segments"]
        ]
    }


def generate_highlights(transcription: Dict, keywords: List[str]) -> List[Dict]:
    """Generate highlights based on keywords in the transcription."""
    highlights = []
    
    for segment in transcription["segments"]:
        segment_text = segment["text"].lower()
        
        for keyword in keywords:
            if keyword.lower() in segment_text:
                highlights.append({
                    "keyword": keyword,
                    "segment_id": segment["id"],
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"],
                    "context": segment["text"]
                })
    
    return highlights


@app.get("/")
async def root():
    return {
        "service": "Audio Transcription Service",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/audio/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """Transcribe audio file."""
    # Check file extension
    allowed_extensions = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Save uploaded file
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}{file_ext}"
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    try:
        # Transcribe audio
        result = transcribe_audio(str(file_path))
        
        # Save transcription result
        result_path = UPLOAD_DIR / f"{file_id}_transcription.json"
        with open(result_path, "w") as f:
            json.dump(result, f)
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "transcription": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@app.post("/audio/highlight")
async def create_highlights(
    file: UploadFile = File(...),
    keywords: str = ""
):
    """Transcribe audio and generate highlights for keywords."""
    # Check file extension
    allowed_extensions = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Parse keywords
    keyword_list = [kw.strip() for kw in keywords.split(",") if kw.strip()]
    
    if not keyword_list:
        raise HTTPException(status_code=400, detail="No keywords provided")
    
    # Save uploaded file
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}{file_ext}"
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    try:
        # Transcribe audio
        transcription = transcribe_audio(str(file_path))
        
        # Generate highlights
        highlights = generate_highlights(transcription, keyword_list)
        
        result = {
            "file_id": file_id,
            "filename": file.filename,
            "transcription": transcription,
            "highlights": highlights,
            "keywords": keyword_list
        }
        
        # Save result
        result_path = UPLOAD_DIR / f"{file_id}_highlights.json"
        with open(result_path, "w") as f:
            json.dump(result, f)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.get("/audio/result/{file_id}")
async def get_result(file_id: str):
    """Get transcription or highlight result."""
    # Try to find transcription or highlights file
    transcription_path = UPLOAD_DIR / f"{file_id}_transcription.json"
    highlights_path = UPLOAD_DIR / f"{file_id}_highlights.json"
    
    if highlights_path.exists():
        with open(highlights_path, "r") as f:
            return json.load(f)
    elif transcription_path.exists():
        with open(transcription_path, "r") as f:
            return json.load(f)
    else:
        raise HTTPException(status_code=404, detail="Result not found")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "audio-service"}
