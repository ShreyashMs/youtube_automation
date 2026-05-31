import os
import traceback
from datetime import datetime

from scripts.script_generator import generate_script
from scripts.metadata_generator import generate_metadata
from scripts.tts_generator import generate_voice
from scripts.fetch_footage import fetch_footage
from scripts.editor import create_video
from scripts.youtube_uploader import upload_video

from scripts.thumbnail_generator import (
    create_thumbnail
)

from scripts.analytics_tracker import (
    save_video_data
)

# ---------------------------------------------------
# PATHS
# ---------------------------------------------------

SCRIPT_PATH = "script.txt"

VIDEO_OUTPUT = "output/final_short.mp4"

THUMBNAIL_OUTPUT = "output/thumbnail.jpg"

# ---------------------------------------------------
# CLEAN TEXT
# ---------------------------------------------------

def clean_text(text):

    return (
        text.replace("**", "")
        .replace('"', "")
        .strip()
    )

# ---------------------------------------------------
# VERIFY FILE
# ---------------------------------------------------

def verify_file(path, message):

    if not os.path.exists(path):

        raise FileNotFoundError(message)

# ---------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------

def run_pipeline():

    print("\n" + "=" * 60)
    print("STARTING AUTOMATED SHORTS PIPELINE")
    print("=" * 60)

    start_time = datetime.now()

    # ---------------------------------------------------
    # GENERATE SCRIPT
    # ---------------------------------------------------

    print("\nGenerating script...\n")

    script = generate_script()

    if not script:

        raise ValueError(
            "Script generation failed"
        )

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

    print("\nScript generated successfully!")

    # ---------------------------------------------------
    # GENERATE METADATA
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

    full_description = description

    print("\nTITLE:\n")
    print(title)

    print("\nDESCRIPTION:\n")
    print(full_description)

    # ---------------------------------------------------
    # THUMBNAIL
    # ---------------------------------------------------

    print("\nGenerating thumbnail...\n")

    create_thumbnail(title)

    verify_file(

        THUMBNAIL_OUTPUT,

        "Thumbnail missing"
    )

    print("\nThumbnail created successfully!")

    # ---------------------------------------------------
    # FETCH FOOTAGE
    # ---------------------------------------------------

    print("\nFetching footage...\n")

    footage_count = fetch_footage(script)

    if footage_count < 3:

        raise Exception(
            "Not enough footage downloaded"
        )

    print(
        f"\nDownloaded {footage_count} clips"
    )

    # ---------------------------------------------------
    # GENERATE VOICE
    # ---------------------------------------------------

    print("\nGenerating voice...\n")

    generate_voice()

    verify_file(

        "assets/audio/narration.wav",

        "Narration missing"
    )

    print("\nVoice generated successfully!")

    # ---------------------------------------------------
    # CREATE VIDEO
    # ---------------------------------------------------

    print("\nCreating final video...\n")

    create_video()

    verify_file(

        VIDEO_OUTPUT,

        "Final video missing"
    )

    print(
        "\nFinal video created successfully!"
    )

    # ---------------------------------------------------
    # UPLOAD TO YOUTUBE
    # ---------------------------------------------------

    print("\nUploading to YouTube...\n")

    upload_result = upload_video(

        title=title,

        description=full_description,

        video_path=VIDEO_OUTPUT
    )

    print("\nVideo uploaded successfully!")

    # ---------------------------------------------------
    # SAVE ANALYTICS
    # ---------------------------------------------------

    save_video_data(

        title=title,

        topic=script[:40],

        video_id=upload_result["video_id"],

        video_url=upload_result["video_url"]
    )

    print("\nAnalytics saved!")

    # ---------------------------------------------------
    # FINISH
    # ---------------------------------------------------

    end_time = datetime.now()

    total_time = (
        end_time - start_time
    ).total_seconds()

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED")
    print(
        f"TOTAL TIME: {round(total_time, 2)} seconds"
    )
    print("=" * 60)

# ---------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------

if __name__ == "__main__":

    try:

        run_pipeline()

    except KeyboardInterrupt:

        print("\nPipeline stopped manually.")

    except Exception as e:

        print("\nPIPELINE FAILED")
        print(e)

        traceback.print_exc()