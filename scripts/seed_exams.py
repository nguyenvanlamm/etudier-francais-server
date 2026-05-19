#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, Base, engine
from app.models.exam import Exam
from app.routers.exams import MOCK_EXAMS, MOCK_QUESTIONS, generate_sample_questions


def seed_exams():
    print("Starting exam seeding...")
    
    db = SessionLocal()
    
    try:
        existing_count = db.query(Exam).count()
        print(f"Current exams in DB: {existing_count}")
        
        for exam_data in MOCK_EXAMS:
            existing = db.query(Exam).filter(Exam.id == exam_data["id"]).first()
            if existing:
                print(f"Exam {exam_data['id']} already exists, skipping...")
                continue
            
            exam = Exam(
                id=exam_data["id"],
                course_slug=exam_data["courseSlug"],
                name=exam_data["name"],
                duration=exam_data["duration"],
                question_count=exam_data["questionCount"],
                difficulty=exam_data["difficulty"],
                skills=exam_data["skills"]
            )
            db.add(exam)
            print(f"Added exam: {exam_data['id']} - {exam_data['name']}")
        
        db.commit()
        
        final_count = db.query(Exam).count()
        print(f"\nSeeding completed!")
        print(f"Total exams in DB: {final_count}")
        
        print("\n--- Sample Questions Summary ---")
        for exam_id, questions in MOCK_QUESTIONS.items():
            print(f"{exam_id}: {len(questions)} questions")
        
        extra_exams = [e for e in MOCK_EXAMS if e["id"] not in MOCK_QUESTIONS]
        print(f"\nExams without custom questions: {len(extra_exams)}")
        print("These will use generated sample questions.")
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_exams()