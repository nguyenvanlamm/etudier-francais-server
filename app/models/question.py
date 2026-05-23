from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(String, ForeignKey("exams.id"), nullable=False, index=True)
    external_id = Column(String, nullable=True)
    skill = Column(String, nullable=False)
    type = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    instruction = Column(Text, default="")
    options = Column(JSON, nullable=True)
    correct_answer = Column(String, nullable=False)
    points = Column(Integer, default=1)
    audio_url = Column(String, nullable=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
