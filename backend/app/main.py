from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from sqlalchemy.orm import Session

from app.orchestrator import analyze_code
from app.database import get_db, init_db
from app.models.analysis import AnalysisRecord

app = FastAPI(title="Multi-Agent Code Analyzer API")


@app.on_event("startup")
def on_startup():
    init_db()


# Allow local React dev server and common frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Multi-Agent Code Analyzer backend is running."}


@app.post("/api/analyze")
async def analyze(
    code: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Optional[Session] = Depends(get_db),
):
    """
    Accepts EITHER pasted code (as form field 'code') OR an uploaded .py
    file (as form field 'file'). Runs it through the 5-agent pipeline,
    stores both input code and report in PostgreSQL, and returns the report.
    """
    source_code = ""
    input_type = "paste"
    filename = None

    if file is not None:
        if not file.filename.endswith(".py"):
            raise HTTPException(status_code=400, detail="Only .py files are supported.")
        raw_bytes = await file.read()
        source_code = raw_bytes.decode("utf-8", errors="replace")
        input_type = "upload"
        filename = file.filename
    elif code is not None and code.strip():
        source_code = code
        input_type = "paste"
    else:
        raise HTTPException(
            status_code=400,
            detail="Provide either pasted code ('code' field) or a .py file ('file' field).",
        )

    if not source_code.strip():
        raise HTTPException(status_code=400, detail="The submitted code is empty.")

    report = analyze_code(source_code)

    record_id = None
    created_at = None

    # Persist to PostgreSQL if database connection is available
    if db is not None:
        try:
            record = AnalysisRecord(
                input_type=input_type,
                filename=filename,
                code_content=source_code,
                report=report,
                overall_confidence=report.get("validation", {}).get("overall_confidence"),
                analysis_time_seconds=report.get("timing", {}).get("total_time_seconds"),
            )
            db.add(record)
            db.commit()
            db.refresh(record)
            record_id = record.id
            created_at = record.created_at.isoformat() if record.created_at else None
        except Exception as e:
            db.rollback()
            print(f"[DATABASE ERROR] Failed to save analysis record: {e}")

    report["db_record"] = {
        "id": record_id,
        "saved": record_id is not None,
        "created_at": created_at,
        "input_type": input_type,
        "filename": filename,
    }

    return report


@app.get("/api/history")
def get_history(limit: int = 20, db: Optional[Session] = Depends(get_db)):
    """
    Returns recent code analysis history stored in PostgreSQL.
    """
    if db is None:
        return {"items": [], "database_connected": False}

    records = db.query(AnalysisRecord).order_by(AnalysisRecord.created_at.desc()).limit(limit).all()
    items = []
    for r in records:
        items.append({
            "id": r.id,
            "input_type": r.input_type,
            "filename": r.filename,
            "snippet": r.code_content[:120] + ("..." if len(r.code_content) > 120 else ""),
            "overall_confidence": r.overall_confidence,
            "analysis_time_seconds": r.analysis_time_seconds,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        })
    return {"items": items, "database_connected": True}


@app.get("/api/history/{analysis_id}")
def get_history_detail(analysis_id: int, db: Optional[Session] = Depends(get_db)):
    """
    Fetches a specific stored analysis report and code input by ID.
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection is not available.")

    record = db.query(AnalysisRecord).filter(AnalysisRecord.id == analysis_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Analysis record #{analysis_id} not found.")

    return record.to_dict()
