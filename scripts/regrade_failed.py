"""Re-run AI grading for all exam results with ai_grading_status='failed'."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.exam import Exam, ExamResult
from app.models.question import Question
from app.services.ai_grading import grade_writing_speaking_sync


def _get_questions_from_db(db, exam_id: str) -> list:
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


def main():
    db = SessionLocal()
    try:
        failed = db.query(ExamResult).filter(
            ExamResult.ai_grading_status == "failed"
        ).all()

        if not failed:
            print("No failed results to re-grade.")
            return

        print(f"Found {len(failed)} failed result(s):")
        for r in failed:
            print(f"  ID={r.id}, exam={r.exam_id}, score={r.score}/{r.max_score}")

        for r in failed:
            questions = _get_questions_from_db(db, r.exam_id)
            if not questions:
                exam = db.query(Exam).filter(Exam.id == r.exam_id).first()
                if exam and exam.skills:
                    from app.services.exam_generator import generate_sample_questions
                    questions = generate_sample_questions(r.exam_id, exam.skills)

            print(f"\nRe-grading result ID={r.id} ({r.exam_id})...")
            grade_writing_speaking_sync(
                r.exam_id,
                r.id,
                questions,
                r.answers,
            )
            print(f"  Done.")

    finally:
        db.close()


if __name__ == "__main__":
    main()
