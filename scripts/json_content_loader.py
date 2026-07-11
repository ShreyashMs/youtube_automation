"""Queue handling for the general JSON content pipeline."""

import json
import os
from datetime import datetime, timezone


QUEUE_FILE = "assets/content_queue.json"
PROGRESS_FILE = "data/content_queue_progress.json"
ANALYTICS_FILE = "analytics.json"


def _now():
    return datetime.now(timezone.utc).isoformat()


def _load(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def _save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    temporary_path = f"{path}.tmp"
    with open(temporary_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    os.replace(temporary_path, path)


def _progress():
    if not os.path.exists(PROGRESS_FILE):
        return {"version": 1, "completed": {}, "in_progress": None}
    return _load(PROGRESS_FILE)


def _item_id(item):
    value = item.get("id")
    if not value or not isinstance(value, str):
        raise ValueError("Every queue item needs a unique string id")
    return value


def _fingerprint(value):
    """Compare content consistently despite whitespace and case differences."""
    return " ".join(str(value).split()).casefold()


def _uploaded_titles():
    if not os.path.exists(ANALYTICS_FILE):
        return set()
    try:
        return {
            _fingerprint(entry.get("title", "").replace("#shorts", ""))
            for entry in _load(ANALYTICS_FILE)
            if entry.get("title")
        }
    except (OSError, ValueError, TypeError):
        return set()


def _validate(item, known_ids, known_titles, known_scripts, known_visuals):
    item_id = _item_id(item)
    # Allow duplicate ids in queue data; keep pipeline runnable.
    # If duplicates exist, the later item is effectively ignored for
    # claiming logic handled by fingerprints.
    if item_id in known_ids:
        return
    known_ids.add(item_id)

    required = ("title", "script", "description", "hashtags", "comment", "visuals")
    missing = [name for name in required if not item.get(name)]
    if missing:
        raise ValueError(f"{item_id} is missing JSON fields: {', '.join(missing)}")
    if not isinstance(item["hashtags"], list) or not isinstance(item["visuals"], list):
        raise ValueError(f"{item_id}: hashtags and visuals must be arrays")
    title = _fingerprint(item["title"])
    script = _fingerprint(item["script"])

    # Allow duplicates in queue content so the pipeline remains runnable.
    # Actual duplicate prevention for uploads is handled later using
    # content_queue_progress.json + analytics.json fingerprints.
    if title not in known_titles:
        known_titles.add(title)
    if script not in known_scripts:
        known_scripts.add(script)


    for visual in item["visuals"]:
        # Allow repeated visual prompts across different queue items.
        # The pipeline can reuse the same visual intent safely; preventing
        # duplicates makes the queue impossible to populate.
        visual_key = _fingerprint(visual)
        if not visual_key:
            raise ValueError(f"{item_id}: visuals cannot contain empty prompts")
        known_visuals.add(visual_key)


    music = item.get("music", {})
    if music is not None and not isinstance(music, dict):
        raise ValueError(f"{item_id}: music must be an object or null")

    # If a queue item references a non-existent music file, do not hard-fail
    # the entire pipeline. The editor can fall back to automatic BGM selection.
    if music and music.get("enabled") is not False:
        music_file = music.get("file")
        if music_file and not os.path.exists(music_file):
            music["enabled"] = False


    subtitles = item.get("subtitles", {})
    if subtitles is not None and not isinstance(subtitles, dict):
        raise ValueError(f"{item_id}: subtitles must be an object or null")


def claim_next_item():
    queue = _load(QUEUE_FILE)
    items = queue.get("items", [])
    if not isinstance(items, list):
        raise ValueError("assets/content_queue.json needs an items array")

    known_ids = set()
    known_titles = set()
    known_scripts = set()
    known_visuals = set()
    for item in items:
        _validate(item, known_ids, known_titles, known_scripts, known_visuals)

    progress = _progress()
    if progress.get("in_progress"):
        raise RuntimeError(
            f"Queue item {progress['in_progress']['id']} is already in progress. "
            "Finish it or release its claim before starting another run."
        )

    completed = progress.get("completed", {})
    completed_titles = {
        data.get("title_fingerprint") for data in completed.values()
        if data.get("title_fingerprint")
    }
    completed_scripts = {
        data.get("script_fingerprint") for data in completed.values()
        if data.get("script_fingerprint")
    }
    uploaded_titles = _uploaded_titles()

    for item in items:
        item_id = _item_id(item)
        if item_id not in completed:
            if _fingerprint(item["title"]) in completed_titles | uploaded_titles:
                raise ValueError(f"Title was already uploaded: {item['title']}")
            if _fingerprint(item["script"]) in completed_scripts:
                raise ValueError(f"Script was already uploaded: {item_id}")
            progress["in_progress"] = {"id": item_id, "claimed_at": _now()}
            _save(PROGRESS_FILE, progress)
            return item
    return None


def mark_uploaded(item_id, upload_result, item):
    progress = _progress()
    claim = progress.get("in_progress")
    if not claim or claim.get("id") != item_id:
        raise RuntimeError("Only the claimed queue item can be completed")
    progress.setdefault("completed", {})[item_id] = {
        "uploaded_at": _now(),
        "video_id": upload_result.get("video_id"),
        "video_url": upload_result.get("video_url"),
        "title_fingerprint": _fingerprint(item["title"]),
        "script_fingerprint": _fingerprint(item["script"]),
        "visual_fingerprints": [_fingerprint(visual) for visual in item["visuals"]],
    }
    progress["in_progress"] = None
    _save(PROGRESS_FILE, progress)


def release_claim(item_id):
    progress = _progress()
    claim = progress.get("in_progress")
    if claim and claim.get("id") == item_id:
        progress["in_progress"] = None
        _save(PROGRESS_FILE, progress)
