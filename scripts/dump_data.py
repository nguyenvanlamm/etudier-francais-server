#!/usr/bin/env python3
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.exam import Exam
from app.models.question import Question
from sqlalchemy import inspect


def dump_table_to_dicts(model):
    db = SessionLocal()
    try:
        rows = db.query(model).all()
        result = []
        for row in rows:
            row_dict = {}
            for column in inspect(model).c:
                value = getattr(row, column.name)
                if isinstance(value, datetime):
                    value = value.isoformat()
                row_dict[column.name] = value
            result.append(row_dict)
        return result
    finally:
        db.close()


def main():
    print("Dumping exams...")
    exams = dump_table_to_dicts(Exam)
    print(f"  {len(exams)} exams found")

    print("Dumping questions...")
    questions = dump_table_to_dicts(Question)
    print(f"  {len(questions)} questions found")

    data = {
        "exams": exams,
        "questions": questions,
    }

    output_path = os.path.join(os.path.dirname(__file__), "seed_data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)

    print(f"\nData dumped to {output_path}")


if __name__ == "__main__":
    main()
