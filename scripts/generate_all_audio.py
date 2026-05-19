import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import edge_tts
from app.routers.exams import MOCK_QUESTIONS

VOICE = "fr-FR-HenriNeural"
BASE_DIR = Path(__file__).parent.parent
TEMP_DIR = BASE_DIR / "temp_audio_generate"
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
    print("Starting audio generation for all listening questions...")
    print(f"Voice: {VOICE}")
    print(f"Temp directory: {TEMP_DIR}")
    print()

    total_generated = 0
    total_skipped = 0
    total_failed = 0

    for exam_id, questions in MOCK_QUESTIONS.items():
        print(f"Processing exam: {exam_id}")
        
        for q in questions:
            if q.get("skill") != "listening":
                continue
            
            audio_url = q.get("audioUrl")
            if not audio_url:
                print(f"  - {q.get('id')}: No audioUrl, skipping")
                total_skipped += 1
                continue
            
            question_id = q.get("id")
            content = q.get("content", "")
            
            if not content:
                print(f"  - {question_id}: No content, skipping")
                total_skipped += 1
                continue
            
            audio_filename = f"{question_id}.mp3"
            audio_path = TEMP_DIR / audio_filename
            
            print(f"  - {question_id}: Generating audio...")
            
            success = await generate_audio(content, str(audio_path))
            
            if success and audio_path.exists():
                target_path = BASE_DIR / "assets" / "audio" / exam_id / audio_filename
                target_path.parent.mkdir(parents=True, exist_ok=True)
                audio_path.rename(target_path)
                print(f"    Saved to: {target_path}")
                total_generated += 1
            else:
                print(f"    Generation failed")
                total_failed += 1
    
    print()
    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total generated: {total_generated}")
    print(f"Total skipped: {total_skipped}")
    print(f"Total failed: {total_failed}")


if __name__ == "__main__":
    asyncio.run(main())