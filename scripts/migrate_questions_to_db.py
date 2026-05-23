#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, Base, engine
from app.models.question import Question
from app.models.exam import Exam
from app.routers.exams import MOCK_QUESTIONS, LEVEL_LS_QUESTIONS


def _get_level_from_exam_id(exam_id: str) -> str:
    if exam_id.startswith("delf-a1"):
        return "A1"
    if exam_id.startswith("delf-a2"):
        return "A2"
    if exam_id.startswith("delf-b1"):
        return "B1"
    if exam_id.startswith("delf-b2"):
        return "B2"
    if exam_id.startswith("dalf-c1"):
        return "C1"
    if exam_id.startswith("dalf-c2"):
        return "C2"
    if exam_id.startswith("tcf"):
        return "B2"
    return "B1"


def migrate():
    db = SessionLocal()
    try:
        # Clear existing questions
        db.query(Question).delete()
        db.commit()

        exam_count = db.query(Exam).count()
        print(f"Exams in DB: {exam_count}")

        total_inserted = 0

        for exam_id, questions in MOCK_QUESTIONS.items():
            level = _get_level_from_exam_id(exam_id)
            ls_questions = LEVEL_LS_QUESTIONS.get(level, [])

            # Find position to insert LS (after last listening)
            insert_pos = 0
            for i, q in enumerate(questions):
                if q.get("skill") == "listening":
                    insert_pos = i + 1

            # Build full question list with LS injected
            all_questions = list(questions)
            for i, ls_q in enumerate(ls_questions):
                all_questions.insert(insert_pos + i, ls_q)

            for idx, q in enumerate(all_questions):
                question = Question(
                    exam_id=exam_id,
                    external_id=q.get("id"),
                    skill=q.get("skill", ""),
                    type=q.get("type", ""),
                    content=q.get("content", ""),
                    instruction=q.get("instruction", ""),
                    options=q.get("options"),
                    correct_answer=q.get("correctAnswer", ""),
                    points=q.get("points", 1),
                    audio_url=q.get("audioUrl"),
                    order_index=idx,
                )
                db.add(question)
                total_inserted += 1

            print(f"  {exam_id}: {len(all_questions)} questions (listening_pos={insert_pos})")

        db.commit()
        print(f"\nTotal questions inserted: {total_inserted}")
        print("Migration completed successfully!")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    migrate()
