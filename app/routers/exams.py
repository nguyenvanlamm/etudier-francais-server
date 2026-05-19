from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any
from app.database import get_db
from app.models.user import User
from app.models.exam import Exam, ExamResult
from app.schemas.exam import ExamSubmitRequest, ExamReviewResponse
from app.routers.auth import get_current_user

router = APIRouter(prefix="/tests", tags=["exams"])

MOCK_EXAMS = [
    {
        "id": "delf-a1-full-1",
        "courseSlug": "delf-a1",
        "name": "DELF A1 - Đề số 1",
        "duration": 80,
        "questionCount": 50,
        "difficulty": "easy",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "status": "in_progress",
        "attempts": 1,
        "highestScore": 72
    },
    {
        "id": "delf-a1-full-2",
        "courseSlug": "delf-a1",
        "name": "DELF A1 - Đề số 2",
        "duration": 80,
        "questionCount": 50,
        "difficulty": "medium",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "status": "not_started",
        "attempts": 0
    },
    {
        "id": "delf-a2-full-1",
        "courseSlug": "delf-a2",
        "name": "DELF A2 - Đề số 1",
        "duration": 100,
        "questionCount": 60,
        "difficulty": "easy",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "status": "completed",
        "attempts": 2,
        "highestScore": 88
    },
    {
        "id": "delf-b1-full-1",
        "courseSlug": "delf-b1",
        "name": "DELF B1 - Đề số 1",
        "duration": 115,
        "questionCount": 70,
        "difficulty": "medium",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "status": "not_started",
        "attempts": 0
    },
    {
        "id": "delf-b2-full-1",
        "courseSlug": "delf-b2",
        "name": "DELF B2 - Đề số 1",
        "duration": 150,
        "questionCount": 80,
        "difficulty": "medium",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "status": "in_progress",
        "attempts": 1,
        "highestScore": 65
    },
    {
        "id": "dalf-c1-full-1",
        "courseSlug": "dalf-c1",
        "name": "DALF C1 - Đề số 1",
        "duration": 240,
        "questionCount": 80,
        "difficulty": "hard",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "status": "not_started",
        "attempts": 0
    },
    {
        "id": "dalf-c2-full-1",
        "courseSlug": "dalf-c2",
        "name": "DALF C2 - Đề số 1",
        "duration": 210,
        "questionCount": 60,
        "difficulty": "hard",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "status": "not_started",
        "attempts": 0
    },
    {
        "id": "tcf-full-1",
        "courseSlug": "tcf",
        "name": "TCF - Đề số 1",
        "duration": 150,
        "questionCount": 100,
        "difficulty": "medium",
        "skills": {"listening": 33, "reading": 33, "writing": 0, "speaking": 34},
        "status": "not_started",
        "attempts": 0
    }
]

MOCK_QUESTIONS = {
    "delf-a1-full-1": [
        {
            "id": "q1",
            "skill": "listening",
            "type": "multiple_choice",
            "content": "Ecoutez la conversation et répondez.",
            "instruction": "Qu'est-ce que Marie fait ce week-end?",
            "options": ["Elle va au cinéma", "Elle fait du shopping", "Elle rencontre des amis", "Elle reste chez elle"],
            "correctAnswer": "Elle va au cinéma",
            "points": 1
        },
        {
            "id": "q2",
            "skill": "listening",
            "type": "multiple_choice",
            "content": "Ecoutez l'annonce et répondez.",
            "instruction": "A quelle heure part le train?",
            "options": ["10h00", "10h15", "10h30", "10h45"],
            "correctAnswer": "10h30",
            "points": 1
        },
        {
            "id": "q3",
            "skill": "reading",
            "type": "multiple_choice",
            "content": "Lisez le texte et répondez.",
            "instruction": "De quelle couleur est la robe?",
            "options": ["Rouge", "Bleue", "Verte", "Jaune"],
            "correctAnswer": "Bleue",
            "points": 1
        },
        {
            "id": "q4",
            "skill": "reading",
            "type": "true_false",
            "content": "Lisez l'email et dites si c'est vrai ou faux.",
            "instruction": "Le rendez-vous est à 14h.",
            "correctAnswer": "true",
            "points": 1
        },
        {
            "id": "q5",
            "skill": "writing",
            "type": "short_answer",
            "content": "Ecrivez une phrase pour présenter votre famille.",
            "instruction": "Utilisez au moins 3 mots.",
            "correctAnswer": "",
            "points": 5
        }
    ]
}


@router.get("")
def get_exams(
    courseSlug: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exams = MOCK_EXAMS.copy()
    if courseSlug:
        exams = [e for e in exams if e["courseSlug"] == courseSlug]

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
    exam = next((e for e in MOCK_EXAMS if e["id"] == examId), None)
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )

    questions = MOCK_QUESTIONS.get(examId, [])

    return {
        **exam,
        "questions": questions
    }


@router.post("/{examId}/submit")
def submit_exam(
    examId: str,
    request: ExamSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exam = next((e for e in MOCK_EXAMS if e["id"] == examId), None)
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )

    questions = MOCK_QUESTIONS.get(examId, [])
    correct_count = 0
    total_points = 0

    for q in questions:
        total_points += q.get("points", 1)
        user_answer = request.answers.get(q["id"], "")
        if q.get("type") in ["short_answer", "essay"]:
            correct_count += q.get("points", 1)
        elif user_answer.lower() == q.get("correctAnswer", "").lower():
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
        started_at=datetime.utcnow(),
        completed_at=datetime.utcnow()
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    return {
        "resultId": str(result.id),
        "score": score,
        "maxScore": max_score,
        "percentage": round(percentage, 1),
        "passed": passed
    }


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

    exam = next((e for e in MOCK_EXAMS if e["id"] == examId), None)
    questions = MOCK_QUESTIONS.get(examId, [])

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
    for q in questions:
        user_answer = result.answers.get(q["id"], "")
        is_correct = user_answer.lower() == q.get("correctAnswer", "").lower() if q.get("correctAnswer") else False

        review_questions.append({
            "id": q["id"],
            "skill": q["skill"],
            "type": q["type"],
            "content": q.get("content", ""),
            "instruction": q.get("instruction", ""),
            "options": q.get("options", []),
            "answer": q.get("correctAnswer", ""),
            "explanation": None,
            "audioUrl": None,
            "imageUrl": None,
            "userAnswer": user_answer,
            "isCorrect": is_correct,
            "points": q.get("points", 1)
        })

    return {
        "exam": {
            "id": examId,
            "name": exam["name"] if exam else examId,
            "courseSlug": exam["courseSlug"] if exam else "",
            "courseName": course_names.get(exam["courseSlug"], "") if exam else "",
            "duration": exam["duration"] if exam else 0,
            "totalScore": result.score,
            "maxScore": result.max_score,
            "percentage": result.percentage,
            "passed": result.passed == "true",
            "timeSpent": 0
        },
        "result": {
            "score": result.score,
            "maxScore": result.max_score,
            "percentage": result.percentage,
            "passed": result.passed == "true",
            "details": {
                "listening": {"correct": 2, "total": 2},
                "reading": {"correct": 2, "total": 2},
                "writing": {"correct": 1, "total": 1}
            },
            "startedAt": result.started_at.isoformat() if result.started_at else "",
            "completedAt": result.completed_at.isoformat() if result.completed_at else ""
        },
        "questions": review_questions,
        "userAnswers": result.answers
    }