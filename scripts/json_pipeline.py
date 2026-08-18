"""General JSON queue pipeline used by ``python main.py``."""

import os
from datetime import datetime

from scripts.analytics_tracker import save_video_data
from scripts.editor import create_video
from scripts.fetch_footage import fetch_footage
from scripts.json_content_loader import claim_next_item, mark_uploaded, release_claim
from scripts.thumbnail_generator import create_thumbnail
from scripts.tts_generator import generate_voice
from scripts.youtube_uploader import post_comment, upload_video


SCRIPT_PATH = "script.txt"
VIDEO_OUTPUT = "output/final_short.mp4"
THUMBNAIL_OUTPUT = "output/thumbnail.jpg"


def _save_script(script):
    with open(SCRIPT_PATH, "w", encoding="utf-8") as file:
        file.write(script.strip())


def _require_file(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Expected output is missing: {path}")


def _description(item):
    tags = [str(tag) if str(tag).startswith("#") else f"#{tag}" for tag in item["hashtags"]]
    return f"{item['description'].strip()}\n\n{' '.join(dict.fromkeys(tags))}"


def run_json_pipeline():
    item = claim_next_item()
    if not item:
        print("No unexecuted item in assets/content_queue.json.")
        return

    item_id = item["id"]
    started_at = datetime.now()
    try:
        print(f"Running JSON queue item: {item_id} ({item.get('emotion', 'neutral')})")
        print(f"Title: {item['title']}")
        
        # Step tracking for resumable pipelines
        print("\n[STEP 1/6] Saving script...")
        _save_script(item["script"])
        _require_file(SCRIPT_PATH)
        print("✓ Script saved")

        print("[STEP 2/6] Creating thumbnail...")
        create_thumbnail(item["title"])
        _require_file(THUMBNAIL_OUTPUT)
        print("✓ Thumbnail created")

        print("[STEP 3/6] Fetching footage...")
        count = fetch_footage(item["script"], item["visuals"])
        if count < 3:
            raise RuntimeError("Not enough new footage downloaded")
        print(f"✓ Footage fetched ({count} clips)")

        print("[STEP 4/6] Generating voice...")
        generate_voice(item.get("voice"))
        _require_file("assets/audio/narration.wav")
        print("✓ Voice generated")
        
        print("[STEP 5/6] Creating video...")
        create_video({
            "emotion": item.get("emotion", "neutral"),
            "music": item.get("music", {}),
            "subtitles": item.get("subtitles", {"enabled": True}),
        })
        _require_file(VIDEO_OUTPUT)
        print("✓ Video created")

        print("[STEP 6/6] Uploading video...")
        upload_result = upload_video(
            title=item["title"],
            description=_description(item),
            video_path=VIDEO_OUTPUT,
            tags=[tag.lstrip("#") for tag in item["hashtags"]],
            playlist_id=item.get("playlist_id"),
        )
        if not upload_result or not upload_result.get("video_id"):
            raise RuntimeError("Upload failed or did not return a video id")
        print(f"✓ Video uploaded - ID: {upload_result.get('video_id')}")

        # Prevent duplicates as soon as the upload is confirmed.
        mark_uploaded(item_id, upload_result, item)
        try:
            post_comment(upload_result["video_id"], item["comment"])
            save_video_data(item["title"], item_id, upload_result["video_id"], upload_result.get("video_url", ""))
        except Exception as follow_up_error:
            print(f"Upload is complete; optional follow-up failed: {follow_up_error}")

        elapsed = (datetime.now() - started_at).total_seconds()
        print(f"\n✓ JSON pipeline completed in {elapsed:.1f} seconds.")
    except BaseException as e:
        elapsed = (datetime.now() - started_at).total_seconds()
        print(f"\n✗ Pipeline interrupted after {elapsed:.1f} seconds")
        print(f"  Error: {str(e)}")
        print(f"  Task {item_id} will resume from the last failed step when pipeline runs again.")
        release_claim(item_id)
        raise
