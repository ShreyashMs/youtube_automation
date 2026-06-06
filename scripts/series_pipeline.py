import os
import sys
import traceback
from datetime import datetime

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from same directory (scripts)
from content_loader import (
    get_next_episode,
    mark_episode_uploaded
)

from fetch_footage import (
    fetch_footage
)

from tts_generator import (
    generate_voice
)

from editor import (
    create_video
)

from thumbnail_generator import (
    create_thumbnail
)

from comment_generator import (
    generate_comment
)

from youtube_uploader import (
    upload_video,
    post_comment
)

from analytics_tracker import (
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

    if not text:
        return ""

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
# SAVE SCRIPT
# ---------------------------------------------------

def save_script(script):

    with open(

        SCRIPT_PATH,

        "w",

        encoding="utf-8"

    ) as f:

        f.write(script)

# ---------------------------------------------------
# PRINT SECTION
# ---------------------------------------------------

def print_section(title):

    print("\n" + "=" * 60)

    print(title)

    print("=" * 60)

# ---------------------------------------------------
# MAIN SERIES PIPELINE
# ---------------------------------------------------

def run_series_pipeline():

    start_time = datetime.now()

    print_section(
        "STARTING SERIES PIPELINE"
    )

    # ---------------------------------------------------
    # LOAD NEXT EPISODE
    # ---------------------------------------------------

    episode = get_next_episode()

    if not episode:

        raise Exception(
            "No episode found"
        )

    series_name = episode.get(
        "series",
        "unknown_series"
    )

    episode_number = episode.get(
        "episode",
        1
    )

    title = clean_text(
        episode.get(
            "title",
            "Untitled"
        )
    )

    hook = clean_text(
        episode.get(
            "hook",
            ""
        )
    )

    script = clean_text(
        episode.get(
            "script",
            ""
        )
    )

    full_script = f"{hook}\n\n{script}"

    # ---------------------------------------------------
    # SAVE SCRIPT
    # ---------------------------------------------------

    print("\nSaving script...\n")

    save_script(full_script)

    verify_file(
        SCRIPT_PATH,
        "script.txt missing"
    )

    print("\nScript saved!")

    # ---------------------------------------------------
    # DESCRIPTION
    # ---------------------------------------------------

    description = f"""
{title}

यह वीडियो हमारी {series_name} श्रृंखला का हिस्सा है।

पूरी श्रृंखला देखने के लिए प्लेलिस्ट जरूर देखें।

#bhagavadgita #shorts #geeta
""".strip()

    # ---------------------------------------------------
    # THUMBNAIL
    # ---------------------------------------------------

    print("\nGenerating thumbnail...\n")

    create_thumbnail(title)

    verify_file(
        THUMBNAIL_OUTPUT,
        "Thumbnail missing"
    )

    print(
        "\nThumbnail created!"
    )

    # ---------------------------------------------------
    # FETCH FOOTAGE
    # ---------------------------------------------------

    print("\nFetching footage...\n")

    footage_count = fetch_footage(
        full_script
    )

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

    print(
        "\nVoice generated!"
    )

    # ---------------------------------------------------
    # CREATE VIDEO
    # ---------------------------------------------------

    print("\nCreating video...\n")

    create_video()

    verify_file(
        VIDEO_OUTPUT,
        "Final video missing"
    )

    print(
        "\nVideo created!"
    )

    # ---------------------------------------------------
    # UPLOAD VIDEO
    # ---------------------------------------------------

    print("\nUploading video...\n")

    upload_result = upload_video(

        title=title,

        description=description,

        video_path=VIDEO_OUTPUT
    )

    if not upload_result:

        raise Exception(
            "Upload failed"
        )

    video_id = upload_result.get(
        "video_id"
    )

    video_url = upload_result.get(
        "video_url"
    )

    if not video_id:

        raise Exception(
            "Missing video_id"
        )

    print("\nUPLOAD SUCCESSFUL")

    print(video_url)

    # ---------------------------------------------------
    # GENERATE COMMENT
    # ---------------------------------------------------

    print("\nGenerating comment...\n")

    comment = generate_comment(
        full_script
    )

    print("\nPosting comment...\n")

    post_comment(

        video_id=video_id,

        comment_text=comment
    )

    # ---------------------------------------------------
    # SAVE ANALYTICS
    # ---------------------------------------------------

    print("\nSaving analytics...\n")

    save_video_data(

        title=title,

        topic=series_name,

        video_id=video_id,

        video_url=video_url
    )

    # ---------------------------------------------------
    # MARK EPISODE COMPLETE
    # ---------------------------------------------------

    mark_episode_uploaded(

        series_name,

        episode_number
    )

    # ---------------------------------------------------
    # FINISH
    # ---------------------------------------------------

    end_time = datetime.now()

    total_time = (
        end_time - start_time
    ).total_seconds()

    print_section(
        "SERIES PIPELINE COMPLETED"
    )

    print(
        f"TOTAL TIME: {round(total_time, 2)} seconds"
    )

# ---------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------

if __name__ == "__main__":

    try:

        run_series_pipeline()

    except KeyboardInterrupt:

        print(
            "\nPipeline stopped manually."
        )

    except Exception as e:

        print_section(
            "PIPELINE FAILED"
        )

        print(e)

        traceback.print_exc()