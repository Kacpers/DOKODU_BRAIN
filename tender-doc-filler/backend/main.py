"""FastAPI app for TenderScope Document Filler."""
import uuid
import shutil
import subprocess
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from .models import AnalysisResponse, CompanyProfile, ErrorResponse
from .engines.ai_engine import analyze_ai
from .docx_writer import write_fields
from .profile import load_profile, save_profile

ALLOWED_EXTENSIONS = {".docx", ".doc"}

app = FastAPI(title="Dokodu - Formularze przetargowe", version="0.2.0")

UPLOAD_DIR = Path("/tmp/tender")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# In-memory store for analysis results
_results: dict[str, AnalysisResponse] = {}


@app.post("/api/upload", response_model=AnalysisResponse)
async def upload_and_analyze(
    file: UploadFile = File(...),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail={"error": "No filename provided", "code": "INVALID_FORMAT"},
        )
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail={"error": "Only .docx and .doc files are supported", "code": "INVALID_FORMAT"},
        )

    doc_id = str(uuid.uuid4())
    doc_dir = UPLOAD_DIR / doc_id
    doc_dir.mkdir(parents=True, exist_ok=True)

    source_path = doc_dir / file.filename
    with open(source_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Convert .doc to .docx via LibreOffice
    if ext == ".doc":
        result = subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "docx", "--outdir", str(doc_dir), str(source_path)],
            capture_output=True, timeout=30,
        )
        converted = source_path.with_suffix(".docx")
        if not converted.exists():
            raise HTTPException(
                status_code=422,
                detail={"error": f"Failed to convert .doc to .docx: {result.stderr.decode()[:200]}", "code": "CONVERSION_FAILED"},
            )
        source_path = converted

    profile = load_profile()
    fields = analyze_ai(source_path, profile)

    # Write filled document
    filled_path = doc_dir / f"FILLED_{file.filename}"
    write_fields(source_path, fields, filled_path)

    filled = [f for f in fields if f.filled_value]
    response = AnalysisResponse(
        document_id=doc_id,
        filename=file.filename,
        fields=fields,
        total_fields=len(fields),
        filled_fields=len(filled),
    )
    _results[doc_id] = response
    return response


@app.get("/api/documents/{doc_id}", response_model=AnalysisResponse)
async def get_document(doc_id: str):
    if doc_id not in _results:
        raise HTTPException(
            status_code=404,
            detail={"error": "Document not found", "code": "NOT_FOUND"},
        )
    return _results[doc_id]


@app.get("/api/documents/{doc_id}/download")
async def download_filled(doc_id: str):
    if doc_id not in _results:
        raise HTTPException(
            status_code=404,
            detail={"error": "Document not found", "code": "NOT_FOUND"},
        )
    doc_dir = UPLOAD_DIR / doc_id
    filled_files = list(doc_dir.glob("FILLED_*"))
    if not filled_files:
        raise HTTPException(
            status_code=404,
            detail={"error": "Filled document not found", "code": "NOT_FOUND"},
        )
    return FileResponse(
        filled_files[0],
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=filled_files[0].name,
    )


@app.get("/api/profile", response_model=CompanyProfile)
async def get_profile():
    return load_profile()


@app.put("/api/profile", response_model=CompanyProfile)
async def update_profile(profile: CompanyProfile):
    save_profile(profile)
    return profile
