import json
import os
import logging

from app.database import SessionLocal
from app.models.exam import Exam
from app.models.question import Question

logger = logging.getLogger(__name__)

SEED_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "scripts",
    "seed_data.json",
)


def seed_database():
    db = SessionLocal()
    try:
        exam_count = db.query(Exam).count()
        question_count = db.query(Question).count()

        if exam_count > 0 and question_count > 0:
            logger.info(
                f"Database already seeded: {exam_count} exams, {question_count} questions"
            )
            return

        if not os.path.exists(SEED_DATA_PATH):
            logger.warning(f"Seed data file not found at {SEED_DATA_PATH}")
            return

        with open(SEED_DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        if exam_count == 0:
            for exam_data in data["exams"]:
                existing = db.query(Exam).filter(Exam.id == exam_data["id"]).first()
                if existing:
                    continue
                exam = Exam(
                    id=exam_data["id"],
                    course_slug=exam_data["course_slug"],
                    name=exam_data["name"],
                    duration=exam_data["duration"],
                    question_count=exam_data["question_count"],
                    skills=exam_data["skills"],
                )
                db.add(exam)
            db.commit()
            logger.info(f"Seeded {len(data['exams'])} exams")

        if question_count == 0:
            for q_data in data["questions"]:
                existing = (
                    db.query(Question)
                    .filter(
                        Question.exam_id == q_data["exam_id"],
                        Question.external_id == q_data["external_id"],
                    )
                    .first()
                )
                if existing:
                    continue
                question = Question(
                    exam_id=q_data["exam_id"],
                    external_id=q_data["external_id"],
                    skill=q_data["skill"],
                    type=q_data["type"],
                    content=q_data["content"],
                    instruction=q_data.get("instruction", ""),
                    options=q_data.get("options"),
                    correct_answer=q_data["correct_answer"],
                    points=q_data.get("points", 1),
                    audio_url=q_data.get("audio_url"),
                    order_index=q_data.get("order_index", 0),
                )
                db.add(question)
            db.commit()
            logger.info(f"Seeded {len(data['questions'])} questions")

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()
