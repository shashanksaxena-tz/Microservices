from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
import json
from pathlib import Path
from typing import List, Dict
import uuid
import os

app = FastAPI(title="OCR Service", description="PDF OCR with text highlighting")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/uploads")) / "ocr"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def extract_text_with_coordinates(pdf_path: str) -> Dict:
    """Extract text from PDF with coordinates for each word."""
    doc = fitz.open(pdf_path)
    results = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text_instances = page.get_text("dict")
        
        page_data = {
            "page_number": page_num + 1,
            "width": page.rect.width,
            "height": page.rect.height,
            "blocks": []
        }
        
        for block in text_instances.get("blocks", []):
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        page_data["blocks"].append({
                            "text": span.get("text", ""),
                            "bbox": span.get("bbox", []),
                            "size": span.get("size", 0),
                            "font": span.get("font", "")
                        })
        
        results.append(page_data)
    
    doc.close()
    return {"pages": results, "total_pages": len(results)}


def highlight_pdf(pdf_path: str, search_terms: List[str], output_path: str):
    """Create a highlighted version of the PDF."""
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        for search_term in search_terms:
            text_instances = page.search_for(search_term)
            
            for inst in text_instances:
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors(stroke=[1, 1, 0])  # Yellow highlight
                highlight.update()
    
    doc.save(output_path)
    doc.close()


@app.get("/")
async def root():
    return {
        "service": "OCR Service",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/ocr/extract")
async def extract_text(file: UploadFile = File(...)):
    """Extract text from PDF with coordinates."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Save uploaded file
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}.pdf"
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    try:
        # Extract text with coordinates
        result = extract_text_with_coordinates(str(file_path))
        
        # Save extraction result
        result_path = UPLOAD_DIR / f"{file_id}_result.json"
        with open(result_path, "w") as f:
            json.dump(result, f)
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "extraction": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR extraction failed: {str(e)}")


@app.post("/ocr/highlight")
async def create_highlighted_pdf(
    file: UploadFile = File(...),
    search_terms: str = ""
):
    """Create a highlighted PDF with search terms marked."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Parse search terms
    terms = [term.strip() for term in search_terms.split(",") if term.strip()]
    
    if not terms:
        raise HTTPException(status_code=400, detail="No search terms provided")
    
    # Save uploaded file
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}.pdf"
    highlighted_path = UPLOAD_DIR / f"{file_id}_highlighted.pdf"
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    try:
        # Create highlighted version
        highlight_pdf(str(file_path), terms, str(highlighted_path))
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "highlighted_file": f"{file_id}_highlighted.pdf",
            "search_terms": terms,
            "download_url": f"/ocr/download/{file_id}_highlighted.pdf"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Highlighting failed: {str(e)}")


@app.get("/ocr/download/{filename}")
async def download_file(filename: str):
    """Download processed PDF file."""
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/pdf"
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ocr-service"}
