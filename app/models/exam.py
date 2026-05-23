from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Exam(Base):
    __tablename__ = "exams"

    id = Column(String, primary_key=True, index=True)
    course_slug = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    question_count = Column(Integer, nullable=False)
    skills = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ExamResult(Base):
    __tablename__ = "exam_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    exam_id = Column(String, index=True, nullable=False)
    score = Column(Float, default=0)
    max_score = Column(Float, default=0)
    percentage = Column(Float, default=0)
    passed = Column(String, default="false")
    answers = Column(JSON, default={})
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ai_grading_status = Column(String, default="idle")
    ai_feedback = Column(JSON, default={})