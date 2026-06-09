from pydantic import BaseModel, Field, field_validator
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

    @field_validator("answers")
    @classmethod
    def validate_answers(cls, v: Dict[str, str]) -> Dict[str, str]:
        import re
        for qid, answer in v.items():
            if len(answer) > 10000:
                raise ValueError(f"Answer for question '{qid}' exceeds 10000 characters")
            cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", answer)
            if cleaned != answer:
                v[qid] = cleaned
        return v


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