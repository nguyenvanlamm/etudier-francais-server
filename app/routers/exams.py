from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any, Optional
from app.database import get_db
from app.models.user import User
from app.models.exam import Exam, ExamResult
from app.models.question import Question
from app.schemas.exam import ExamSubmitRequest, ExamReviewResponse
from app.routers.auth import get_current_user as get_user
from app.services.auth import decode_token
from app.services.ai_grading import grade_writing_speaking_sync, _get_level_from_exam_id


security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    if not credentials:
        return None
    
    token = credentials.credentials
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        return None
    
    user_id = payload.get("sub")
    if not user_id:
        return None
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    return user

router = APIRouter(prefix="/tests", tags=["exams"])

MOCK_EXAMS = [
    # DELF A1
    {
        "id": "delf-a1-full-1",
        "courseSlug": "delf-a1",
        "name": "DELF A1 - Đề số 1",
        "duration": 80,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2024-12-01",
    },
    {
        "id": "delf-a1-full-2",
        "courseSlug": "delf-a1",
        "name": "DELF A1 - Đề số 2",
        "duration": 80,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2024-12-10",
    },
    {
        "id": "delf-a1-full-3",
        "courseSlug": "delf-a1",
        "name": "DELF A1 - Đề số 3",
        "duration": 80,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2024-12-20",
    },
    {
        "id": "delf-a1-full-4",
        "courseSlug": "delf-a1",
        "name": "DELF A1 - Đề số 4",
        "duration": 80,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-01-05",
    },
    {
        "id": "delf-a1-full-5",
        "courseSlug": "delf-a1",
        "name": "DELF A1 - Đề số 5",
        "duration": 80,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-01-15",
    },
    {
        "id": "delf-a1-full-6",
        "courseSlug": "delf-a1",
        "name": "DELF A1 - Đề số 6",
        "duration": 80,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-02-01",
    },
    # DELF A2
    {
        "id": "delf-a2-full-1",
        "courseSlug": "delf-a2",
        "name": "DELF A2 - Đề số 1",
        "duration": 100,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2024-12-01",
    },
    {
        "id": "delf-a2-full-2",
        "courseSlug": "delf-a2",
        "name": "DELF A2 - Đề số 2",
        "duration": 100,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2024-12-10",
    },
    {
        "id": "delf-a2-full-3",
        "courseSlug": "delf-a2",
        "name": "DELF A2 - Đề số 3",
        "duration": 100,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2024-12-18",
    },
    {
        "id": "delf-a2-full-4",
        "courseSlug": "delf-a2",
        "name": "DELF A2 - Đề số 4",
        "duration": 100,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-01-08",
    },
    {
        "id": "delf-a2-full-5",
        "courseSlug": "delf-a2",
        "name": "DELF A2 - Đề số 5",
        "duration": 100,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-01-20",
    },
    {
        "id": "delf-a2-full-6",
        "courseSlug": "delf-a2",
        "name": "DELF A2 - Đề số 6",
        "duration": 100,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-02-03",
    },
    # DELF B1
    {
        "id": "delf-b1-full-1",
        "courseSlug": "delf-b1",
        "name": "DELF B1 - Đề số 1",
        "duration": 115,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2024-12-01",
    },
    {
        "id": "delf-b1-full-2",
        "courseSlug": "delf-b1",
        "name": "DELF B1 - Đề số 2",
        "duration": 115,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2024-12-10",
    },
    {
        "id": "delf-b1-full-3",
        "courseSlug": "delf-b1",
        "name": "DELF B1 - Đề số 3",
        "duration": 115,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-01-03",
    },
    {
        "id": "delf-b1-full-4",
        "courseSlug": "delf-b1",
        "name": "DELF B1 - Đề số 4",
        "duration": 115,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-01-18",
    },
    {
        "id": "delf-b1-full-5",
        "courseSlug": "delf-b1",
        "name": "DELF B1 - Đề số 5",
        "duration": 115,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-02-05",
    },
    # DELF B2
    {
        "id": "delf-b2-full-1",
        "courseSlug": "delf-b2",
        "name": "DELF B2 - Đề số 1",
        "duration": 150,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2024-12-01",
    },
    {
        "id": "delf-b2-full-2",
        "courseSlug": "delf-b2",
        "name": "DELF B2 - Đề số 2",
        "duration": 150,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2024-12-10",
    },
    {
        "id": "delf-b2-full-3",
        "courseSlug": "delf-b2",
        "name": "DELF B2 - Đề số 3",
        "duration": 150,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-01-05",
    },
    {
        "id": "delf-b2-full-4",
        "courseSlug": "delf-b2",
        "name": "DELF B2 - Đề số 4",
        "duration": 150,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-01-22",
    },
    {
        "id": "delf-b2-full-5",
        "courseSlug": "delf-b2",
        "name": "DELF B2 - Đề số 5",
        "duration": 150,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-02-06",
    },
    # DALF C1
    {
        "id": "dalf-c1-full-1",
        "courseSlug": "dalf-c1",
        "name": "DALF C1 - Đề số 1",
        "duration": 240,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2024-12-01",
    },
    {
        "id": "dalf-c1-full-2",
        "courseSlug": "dalf-c1",
        "name": "DALF C1 - Đề số 2",
        "duration": 240,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-01-10",
    },
    {
        "id": "dalf-c1-full-3",
        "courseSlug": "dalf-c1",
        "name": "DALF C1 - Đề số 3",
        "duration": 240,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-01-25",
    },
    {
        "id": "dalf-c1-full-4",
        "courseSlug": "dalf-c1",
        "name": "DALF C1 - Đề số 4",
        "duration": 240,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-02-07",
    },
    # DALF C2
    {
        "id": "dalf-c2-full-1",
        "courseSlug": "dalf-c2",
        "name": "DALF C2 - Đề số 1",
        "duration": 210,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2024-12-01",
    },
    {
        "id": "dalf-c2-full-2",
        "courseSlug": "dalf-c2",
        "name": "DALF C2 - Đề số 2",
        "duration": 210,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-01-12",
    },
    {
        "id": "dalf-c2-full-3",
        "courseSlug": "dalf-c2",
        "name": "DALF C2 - Đề số 3",
        "duration": 210,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-01-28",
    },
    {
        "id": "dalf-c2-full-4",
        "courseSlug": "dalf-c2",
        "name": "DALF C2 - Đề số 4",
        "duration": 210,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-02-08",
    },
    # TCF
    {
        "id": "tcf-full-1",
        "courseSlug": "tcf",
        "name": "TCF - Đề số 1",
        "duration": 150,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2024-12-01",
    },
    {
        "id": "tcf-full-2",
        "courseSlug": "tcf",
        "name": "TCF - Đề số 2",
        "duration": 150,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2024-12-10",
    },
    {
        "id": "tcf-full-3",
        "courseSlug": "tcf",
        "name": "TCF - Đề số 3",
        "duration": 150,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-01-06",
    },
    {
        "id": "tcf-full-4",
        "courseSlug": "tcf",
        "name": "TCF - Đề số 4",
        "duration": 150,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-01-20",
    },
    {
        "id": "tcf-full-5",
        "courseSlug": "tcf",
        "name": "TCF - Đề số 5",
        "duration": 150,
        "questionCount": 55,
        "skills": {"listening": 27, "language_structure": 18, "reading": 46, "writing": 5, "speaking": 4},
        "createdAt": "2025-02-04",
    },
]

def generate_sample_questions(exam_id: str, skills: dict) -> list:
    """Generate sample questions based on exam skills."""
    questions = []
    question_types = ["multiple_choice", "true_false", "short_answer"]
    
    skill_map = {
        "listening": "listening",
        "reading": "reading", 
        "writing": "writing",
        "speaking": "speaking",
    }
    
    question_id = 1
    for skill, count in skills.items():
        if count == 0:
            continue
        for i in range(max(1, round(count / 100 * 55))):
            questions.append({
                "id": f"{exam_id}-q{question_id}",
                "skill": skill_map.get(skill, "reading"),
                "type": question_types[i % len(question_types)],
                "content": f"Sample {skill} question {i+1}",
                "instruction": f"Répondez à la question {i+1}",
                "options": ["A", "B", "C", "D"] if question_types[i % len(question_types)] == "multiple_choice" else [],
                "correctAnswer": "A",
                "points": 1
            })
            question_id += 1
    
    return questions


def _get_questions_from_db(db: Session, exam_id: str) -> list:
    """Fetch questions from DB for a given exam, return as dicts."""
    db_questions = db.query(Question).filter(
        Question.exam_id == exam_id
    ).order_by(Question.order_index).all()
    if not db_questions:
        return []
    return [{
        "id": q.external_id or str(q.id),
        "skill": q.skill,
        "type": q.type,
        "content": q.content,
        "instruction": q.instruction,
        "options": q.options,
        "correctAnswer": q.correct_answer,
        "points": q.points,
        "audioUrl": q.audio_url,
    } for q in db_questions]


def exam_to_dict(exam: Exam) -> dict:
    """Convert Exam database object to dictionary."""
    return {
        "id": exam.id,
        "courseSlug": exam.course_slug,
        "name": exam.name,
        "duration": exam.duration,
        "questionCount": exam.question_count,
        "skills": exam.skills,
        "createdAt": exam.created_at.isoformat() if exam.created_at else None,
    }


@router.get("")
def get_exams(
    courseSlug: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Exam)
    if courseSlug:
        query = query.filter(Exam.course_slug == courseSlug)
    
    exams_db = query.all()
    exams = [exam_to_dict(e) for e in exams_db]

    # Only fetch user progress if user is authenticated
    if current_user:
        user_results = db.query(ExamResult).filter(
            ExamResult.user_id == current_user.id
        ).all()

        result_map = {r.exam_id: r for r in user_results}

        for exam in exams:
            if exam["id"] in result_map:
                exam["status"] = "completed"
                exam["attempts"] = result_map[exam["id"]].percentage

    return exams


@router.get("/{examId}")
def get_exam(
    examId: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.config import settings
    
    exam = db.query(Exam).filter(Exam.id == examId).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )

    exam_dict = exam_to_dict(exam)
    
    questions = _get_questions_from_db(db, examId)
    if not questions and exam.skills:
        questions = generate_sample_questions(examId, exam.skills)
    
    # Add full URL for audio files
    base_url = "http://localhost:5000"
    for q in questions:
        if q.get("audioUrl") and q["audioUrl"].startswith("/assets"):
            q["audioUrl"] = f"{base_url}{q['audioUrl']}"

    return {
        **exam_dict,
        "questions": questions
    }


@router.post("/{examId}/submit")
def submit_exam(
    examId: str,
    request: ExamSubmitRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to submit exam"
        )

    exam = db.query(Exam).filter(Exam.id == examId).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )

    questions = _get_questions_from_db(db, examId)
    if not questions and exam.skills:
        questions = generate_sample_questions(examId, exam.skills)

    correct_count = 0
    total_points = 0

    for q in questions:
        total_points += q.get("points", 1)
        user_answer = request.answers.get(q["id"], "")
        if q.get("type") in ["short_answer", "essay"]:
            pass
        else:
            ua = user_answer.lower()
            ca = q.get("correctAnswer", "")
            if q.get("type") == "true_false":
                ua = {"vrai": "true", "faux": "false"}.get(ua, ua)
            if ua == ca.lower():
                correct_count += q.get("points", 1)

    score = correct_count
    max_score = total_points
    percentage = (score / max_score * 100) if max_score > 0 else 0
    passed = percentage >= 50

    result = ExamResult(
        user_id=current_user.id,
        exam_id=examId,
        score=score,
        max_score=max_score,
        percentage=percentage,
        passed=str(passed).lower(),
        answers=request.answers,
        ai_grading_status="pending",
        ai_feedback={},
        started_at=datetime.utcnow(),
        completed_at=datetime.utcnow()
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    background_tasks.add_task(
        grade_writing_speaking_sync,
        examId,
        result.id,
        questions,
        request.answers,
    )

    return {
        "resultId": str(result.id),
        "score": score,
        "maxScore": max_score,
        "percentage": round(percentage, 1),
        "passed": passed,
        "aiGradingStatus": "pending"
    }


@router.get("/{examId}/results/{resultId}/ai-status")
def get_ai_grading_status(
    examId: str,
    resultId: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = db.query(ExamResult).filter(
        ExamResult.id == int(resultId),
        ExamResult.user_id == current_user.id,
        ExamResult.exam_id == examId
    ).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Result not found")

    return {
        "aiGradingStatus": result.ai_grading_status or "idle",
        "aiFeedback": result.ai_feedback or {} if result.ai_grading_status == "completed" else {},
        "score": result.score,
        "maxScore": result.max_score,
        "percentage": result.percentage,
        "passed": result.passed == "true",
    }


@router.post("/{examId}/results/{resultId}/ai-retry")
def retry_ai_grading(
    examId: str,
    resultId: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = db.query(ExamResult).filter(
        ExamResult.id == int(resultId),
        ExamResult.user_id == current_user.id,
        ExamResult.exam_id == examId
    ).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Result not found")

    if result.ai_grading_status != "failed":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot retry: current status is '{result.ai_grading_status}'")

    exam = db.query(Exam).filter(Exam.id == examId).first()
    questions = _get_questions_from_db(db, examId)
    if not questions and exam and exam.skills:
        questions = generate_sample_questions(examId, exam.skills)

    result.ai_grading_status = "pending"
    result.ai_feedback = {}
    db.commit()

    background_tasks.add_task(
        grade_writing_speaking_sync,
        examId,
        result.id,
        questions,
        result.answers,
    )

    return {"aiGradingStatus": "pending"}


@router.get("/{examId}/results/{resultId}/review")
def get_exam_review(
    examId: str,
    resultId: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = db.query(ExamResult).filter(
        ExamResult.id == int(resultId),
        ExamResult.user_id == current_user.id,
        ExamResult.exam_id == examId
    ).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found"
        )

    exam = db.query(Exam).filter(Exam.id == examId).first()
    questions = _get_questions_from_db(db, examId)
    if not questions and exam and exam.skills:
        questions = generate_sample_questions(examId, exam.skills)

    course_names = {
        "delf-a1": "DELF A1",
        "delf-a2": "DELF A2",
        "delf-b1": "DELF B1",
        "delf-b2": "DELF B2",
        "dalf-c1": "DALF C1",
        "dalf-c2": "DALF C2",
        "tcf": "TCF"
    }

    review_questions = []
    ai_feedback = result.ai_feedback or {}
    for q in questions:
        user_answer = result.answers.get(q["id"], "")
        ca = q.get("correctAnswer", "")
        ua = user_answer.lower()
        if q.get("type") == "true_false":
            ua = {"vrai": "true", "faux": "false"}.get(ua, ua)
        is_correct = ua == ca.lower() if ca else False
        fb = ai_feedback.get(q["id"])
        is_correct = fb.get("score", 0) >= 10 if fb and q["skill"] in ("writing", "speaking") else is_correct

        display_answer = ca
        if q.get("type") == "true_false":
            display_answer = {"true": "Vrai", "false": "Faux"}.get(ca.lower(), ca)

        review_questions.append({
            "id": q["id"],
            "skill": q["skill"],
            "type": q["type"],
            "content": q.get("content", ""),
            "instruction": q.get("instruction", ""),
            "options": q.get("options", []),
            "answer": display_answer,
            "explanation": None,
            "audioUrl": None,
            "imageUrl": None,
            "userAnswer": user_answer,
            "isCorrect": is_correct,
            "points": q.get("points", 1),
            "aiFeedback": fb
        })

    return {
        "exam": {
            "id": examId,
            "name": exam.name if exam else examId,
            "courseSlug": exam.course_slug if exam else "",
            "courseName": course_names.get(exam.course_slug, "") if exam else "",
            "duration": exam.duration if exam else 0,
            "totalScore": result.score,
            "maxScore": result.max_score,
            "percentage": result.percentage,
            "passed": result.passed == "true",
            "timeSpent": 0,
            "aiGradingStatus": result.ai_grading_status or "idle"
        },
        "result": {
            "score": result.score,
            "maxScore": result.max_score,
            "percentage": result.percentage,
            "passed": result.passed == "true",
            "details": {
                "listening": {"correct": 2, "total": 2},
                "language_structure": {"correct": 2, "total": 2},
                "reading": {"correct": 2, "total": 2},
                "writing": {"correct": 1, "total": 1},
                "speaking": {"correct": 1, "total": 1}
            },
            "startedAt": result.started_at.isoformat() if result.started_at else "",
            "completedAt": result.completed_at.isoformat() if result.completed_at else ""
        },
        "questions": review_questions,
        "userAnswers": result.answers
    }
