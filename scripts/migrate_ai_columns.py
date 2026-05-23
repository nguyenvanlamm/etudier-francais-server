#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app.models.exam import ExamResult


def migrate():
    Base.metadata.create_all(bind=engine)

    with engine.connect() as conn:
        from sqlalchemy import inspect, text
        inspector = inspect(engine)
        columns = [c["name"] for c in inspector.get_columns("exam_results")]

        if "ai_grading_status" not in columns:
            conn.execute(text(
                "ALTER TABLE exam_results ADD COLUMN ai_grading_status VARCHAR DEFAULT 'idle'"
            ))
            print("Added column: ai_grading_status")
        else:
            print("Column ai_grading_status already exists")

        if "ai_feedback" not in columns:
            conn.execute(text(
                "ALTER TABLE exam_results ADD COLUMN ai_feedback JSON DEFAULT '{}'"
            ))
            print("Added column: ai_feedback")
        else:
            print("Column ai_feedback already exists")

        conn.commit()

    print("Migration completed!")


if __name__ == "__main__":
    migrate()
