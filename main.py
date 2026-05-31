import os
import traceback
from datetime import datetime

from scripts.script_generator import generate_script
from scripts.metadata_generator import generate_metadata
from scripts.tts_generator import generate_voice
from scripts.fetch_footage import fetch_footage
from scripts.editor import create_video
from scripts.youtube_uploader import upload_video

SCRIPT_PATH = "script.txt"

VIDEO_OUTPUT = "output/final_short.mp4"

def clean_text(text):

    return (
        text.replace("**", "")
        .replace('"', "")
        .strip()
    )

def verify_file(path, message):

    if not os.path.exists(path):
        raise FileNotFoundError(message)

def run_pipeline():

    print("\n" + "=" * 60)
    print("STARTING AUTOMATED SHORTS PIPELINE")
    print("=" * 60)

    start_time = datetime.now()

    # ---------------------------------------------------
    # SCRIPT
    # ---------------------------------------------------

    print("\nGenerating script...\n")

    script = generate_script()

    if not script:
        raise ValueError("Script generation failed")

    with open(
        SCRIPT_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(script)

    verify_file(
        SCRIPT_PATH,
        "script.txt missing"
    )

    # ---------------------------------------------------
    # METADATA
    # ---------------------------------------------------

    print("\nGenerating metadata...\n")

    metadata = generate_metadata(script)

    title = clean_text(
        metadata.get(
            "title",
            "पौराणिक रहस्य"
        )
    )

    description = clean_text(
        metadata.get(
            "description",
            "ऐसी और दिव्य कथाओं के लिए रामलला१० को Subscribe करें।"
        )
    )

    hashtags = clean_text(
        metadata.get(
            "hashtags",
            "#राम #महाभारत"
        )
    )

    full_description = (
        f"{description}\n\n{hashtags}"
    )

    print("\nTITLE:")
    print(title)

    print("\nDESCRIPTION:")
    print(full_description)

    # ---------------------------------------------------
    # FOOTAGE
    # ---------------------------------------------------

    print("\nFetching footage...\n")

    footage_count = fetch_footage(script)

    if footage_count < 3:

        raise Exception(
            "Not enough footage downloaded"
        )

    # ---------------------------------------------------
    # VOICE
    # ---------------------------------------------------

    print("\nGenerating voice...\n")

    generate_voice()

    verify_file(
        "assets/audio/narration.wav",
        "Narration missing"
    )

    # ---------------------------------------------------
    # VIDEO
    # ---------------------------------------------------

    print("\nCreating final video...\n")

    create_video()

    verify_file(
        VIDEO_OUTPUT,
        "Final video missing"
    )

    # ---------------------------------------------------
    # UPLOAD
    # ---------------------------------------------------

    print("\nUploading to YouTube...\n")

    upload_video(

        title=title,

        description=full_description,

        video_path=VIDEO_OUTPUT
    )

    end_time = datetime.now()

    total_time = (
        end_time - start_time
    ).total_seconds()

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED")
    print(f"TOTAL TIME: {round(total_time, 2)} seconds")
    print("=" * 60)

if __name__ == "__main__":

    try:

        run_pipeline()

    except Exception as e:

        print("\nPIPELINE FAILED")
        print(e)

        traceback.print_exc()

