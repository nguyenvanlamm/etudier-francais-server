from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class ExamResponse(BaseModel):
    id: str
    courseSlug: str
    name: str
    duration: int
    questionCount: int
    skills: Dict[str, int]
    status: Optional[str] = None
    attempts: int = 0
    highestScore: Optional[float] = None


class ExamSubmitRequest(BaseModel):
    answers: Dict[str, str]
    timeSpent: int


class ExamReviewResponse(BaseModel):
    exam: Dict[str, Any]
    result: Dict[str, Any]
    questions: List[Dict[str, Any]]
    userAnswers: Dict[str, str]


class ContactRequest(BaseModel):
    name: str
    email: str
    subject: str
    message: str