import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import edge_tts
from app.services import storage
from app.routers.exams import MOCK_QUESTIONS

VOICE = "fr-FR-HenriNeural"
TEMP_DIR = Path(__file__).parent.parent / "temp_audio"
TEMP_DIR.mkdir(exist_ok=True)


async def generate_audio(text: str, output_file: str) -> bool:
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(output_file)
        return True
    except Exception as e:
        print(f"Error generating audio: {e}")
        return False


async def main():
    print("Starting audio generation for listening questions...")
    print(f"Voice: {VOICE}")
    print(f"Temp directory: {TEMP_DIR}")
    print()

    total_generated = 0
    total_failed = 0
    results = []

    for exam_id, questions in MOCK_QUESTIONS.items():
        print(f"Processing exam: {exam_id}")
        
        for q in questions:
            if q.get("skill") != "listening":
                continue
            
            question_id = q.get("id")
            content = q.get("content", "")
            
            if not content:
                print(f"  - {question_id}: No content, skipping")
                continue
            
            audio_filename = f"{exam_id}_{question_id}.mp3"
            audio_path = TEMP_DIR / audio_filename
            
            print(f"  - {question_id}: Generating audio...")
            
            success = await generate_audio(content, str(audio_path))
            
            if success and audio_path.exists():
                try:
                    blob_name = f"audio/{exam_id}/{question_id}.mp3"
                    public_url = storage.upload_file(
                        str(audio_path),
                        blob_name
                    )
                    
                    results.append({
                        "exam_id": exam_id,
                        "question_id": question_id,
                        "audioUrl": public_url
                    })
                    
                    print(f"    Uploaded: {public_url}")
                    total_generated += 1
                    
                    audio_path.unlink()
                    
                except Exception as e:
                    print(f"    Upload failed: {e}")
                    total_failed += 1
            else:
                print(f"    Generation failed")
                total_failed += 1
    
    print()
    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total generated: {total_generated}")
    print(f"Total failed: {total_failed}")
    print()
    
    if results:
        print("Results (to update in MOCK_QUESTIONS):")
        print("-" * 50)
        for r in results:
            print(f'"{r["exam_id"]}" -> "{r["question_id"]}": audioUrl = "{r["audioUrl"]}"')
        print()
    
    return results


if __name__ == "__main__":
    asyncio.run(main())