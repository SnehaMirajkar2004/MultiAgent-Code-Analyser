from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON

from app.database import Base


class AnalysisRecord(Base):
    __tablename__ = "analysis_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    input_type = Column(String(20), nullable=False, default="paste")  # 'paste' or 'upload'
    filename = Column(String(255), nullable=True)
    code_content = Column(Text, nullable=False)
    report = Column(JSON, nullable=False)
    overall_confidence = Column(String(50), nullable=True)
    analysis_time_seconds = Column(Float, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "input_type": self.input_type,
            "filename": self.filename,
            "code_content": self.code_content,
            "report": self.report,
            "overall_confidence": self.overall_confidence,
            "analysis_time_seconds": self.analysis_time_seconds,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
