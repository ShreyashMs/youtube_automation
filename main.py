import os
import traceback
from datetime import datetime

from scripts.script_generator import generate_script
from scripts.metadata_generator import generate_metadata
from scripts.tts_generator import generate_voice
from scripts.fetch_footage import fetch_footage
from scripts.editor import create_video

from scripts.thumbnail_generator import (
create_thumbnail
)

from scripts.analytics_tracker import (
save_video_data
)

from scripts.comment_generator import (
generate_comment
)

from scripts.youtube_uploader import (
upload_video,
post_comment
)

from scripts.playlist_config import (
get_playlist_id
)

# ---------------------------------------------------

# OPTIONAL SERIES PIPELINE

# ---------------------------------------------------

try:
    from scripts.content_loader import (
        get_next_episode
    )
except:
    get_next_episode = None


# ---------------------------------------------------

# CONTENT MODE

# ---------------------------------------------------

"""
AVAILABLE MODES:

ai_story (generates AI stories - uploads to shorts playlist)
series (use series_pipeline.py instead for Bhagavad Gita)
"""

CONTENT_MODE = "ai_story"

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
    if not text:
        return ""

    return (
        text.replace("**", "")
        .replace('"', "")
        .replace(""", "")
        .replace(""", "")
        .strip()
)


# ---------------------------------------------------

# VERIFY FILE

# ---------------------------------------------------

def verify_file(path, message):
    if not os.path.exists(path):
        raise FileNotFoundError(message)


# ---------------------------------------------------

# LOAD CONTENT

# ---------------------------------------------------

def load_content():

    # ---------------------------------------------------
    # SERIES PIPELINE
    # ---------------------------------------------------

    if CONTENT_MODE == "series":

        if not get_next_episode:

            raise Exception(
                "series_pipeline.py missing"
            )

        print("\nLoading series episode...\n")

        data = get_next_episode()

        return {

            "script": data.get(
                "script",
                ""
            ),

            "title": data.get(
                "title",
                ""
            ),

            "topic": data.get(
                "title",
                ""
            ),

            "content_type": "series",

            "series": data.get(
                "series",
                "unknown_series"
            ),

            "chapter": data.get(
                "chapter",
                0
            ),

            "episode": data.get(
                "episode",
                0
            )
        }

    # ---------------------------------------------------
    # AI STORY PIPELINE
    # ---------------------------------------------------

    print("\nGenerating AI story...\n")

    script = generate_script()

    return {

        "script": script,

        "title": None,

        "topic": script[:40],

        "content_type": "ai_story",

        "series": None,

        "chapter": None,

        "episode": None
    }


# ---------------------------------------------------

# MAIN PIPELINE

# ---------------------------------------------------

def run_pipeline():

    print("\n" + "=" * 60)
    print("STARTING AUTOMATED SHORTS PIPELINE")
    print("=" * 60)

    start_time = datetime.now()

    # ---------------------------------------------------
    # LOAD CONTENT
    # ---------------------------------------------------

    content = load_content()

    script = content["script"]

    if not script:

        raise ValueError(
            "Script generation failed"
        )

    # ---------------------------------------------------
    # SAVE SCRIPT
    # ---------------------------------------------------

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

    print("\nScript loaded successfully!")

    # ---------------------------------------------------
    # GENERATE METADATA
    # ---------------------------------------------------

    print("\nGenerating metadata...\n")

    # ---------------------------------------------------
    # SERIES CONTENT
    # ---------------------------------------------------

    if content["content_type"] == "series":

        title = clean_text(
            content["title"]
        )

        metadata = generate_metadata(
            script
        )

        description = clean_text(

            metadata.get(

                "description",

                "पूरी श्रृंखला प्लेलिस्ट में देखें।"
            )
        )

        full_description = description

    # ---------------------------------------------------
    # AI STORY CONTENT
    # ---------------------------------------------------

    else:

        metadata = generate_metadata(
            script
        )

        title = clean_text(

            metadata.get(

                "title",

                "पौराणिक रहस्य"
            )
        )

        description = clean_text(

            metadata.get(

                "description",

                "ऐसी और दिव्य कथाओं के लिए Subscribe करें।"
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

    # Determine playlist based on content type
    if content["content_type"] == "series":

        playlist_id = get_playlist_id(content["series"])

    else:

        # AI stories go to the shorts playlist
        playlist_id = get_playlist_id("ai_story")

    upload_result = upload_video(

        title=title,

        description=full_description,

        video_path=VIDEO_OUTPUT,

        playlist_id=playlist_id
    )

    print("\nVideo uploaded successfully!")

    # ---------------------------------------------------
    # GENERATE COMMENT
    # ---------------------------------------------------

    print("\nGenerating comment...\n")

    comment = generate_comment(script)

    # ---------------------------------------------------
    # POST COMMENT
    # ---------------------------------------------------

    print("\nPosting comment...\n")

    post_comment(

        video_id=upload_result["video_id"],

        comment_text=comment
    )

    # ---------------------------------------------------
    # SAVE ANALYTICS
    # ---------------------------------------------------

    save_video_data(

        title=title,

        topic=content["topic"],

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

