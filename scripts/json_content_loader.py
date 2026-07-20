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
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    tmp = f"{path}.tmp"

    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    os.replace(tmp, path)


def _progress():
    if not os.path.exists(PROGRESS_FILE):
        return {
            "version": 1,
            "completed": {},
            "in_progress": None,
        }

    return _load(PROGRESS_FILE)


def _item_id(item):
    value = item.get("id")

    if not value or not isinstance(value, str):
        raise ValueError("Every queue item needs a unique string id")

    return value


def _fingerprint(value):
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

    except Exception:
        return set()


def _validate(item, known_ids, known_titles, known_scripts, known_visuals):
    item_id = _item_id(item)

    if item_id in known_ids:
        return

    known_ids.add(item_id)

    required = (
        "title",
        "script",
        "description",
        "hashtags",
        "comment",
        "visuals",
    )

    missing = [field for field in required if not item.get(field)]

    if missing:
        raise ValueError(
            f"{item_id} is missing fields: {', '.join(missing)}"
        )

    if not isinstance(item["hashtags"], list):
        raise ValueError(f"{item_id}: hashtags must be list")

    if not isinstance(item["visuals"], list):
        raise ValueError(f"{item_id}: visuals must be list")

    title = _fingerprint(item["title"])
    script = _fingerprint(item["script"])

    known_titles.add(title)
    known_scripts.add(script)

    for visual in item["visuals"]:
        visual = _fingerprint(visual)

        if not visual:
            raise ValueError(f"{item_id}: empty visual prompt")

        known_visuals.add(visual)

    music = item.get("music", {})

    if music and music.get("enabled") is not False:
        music_file = music.get("file")

        if music_file and not os.path.exists(music_file):
            music["enabled"] = False


def claim_next_item():
    queue = _load(QUEUE_FILE)

    items = queue.get("items", [])

    if not isinstance(items, list):
        raise ValueError("content_queue.json needs items array")

    known_ids = set()
    known_titles = set()
    known_scripts = set()
    known_visuals = set()

    for item in items:
        _validate(
            item,
            known_ids,
            known_titles,
            known_scripts,
            known_visuals,
        )

    progress = _progress()

    if progress.get("in_progress"):
        raise RuntimeError(
            f"Queue item {progress['in_progress']['id']} is already in progress. "
            "Finish it or release its claim before starting another run."
        )

    completed = progress.get("completed", {})

    completed_titles = {
        data.get("title_fingerprint")
        for data in completed.values()
        if data.get("title_fingerprint")
    }

    completed_scripts = {
        data.get("script_fingerprint")
        for data in completed.values()
        if data.get("script_fingerprint")
    }

    uploaded_titles = _uploaded_titles()

    for item in items:

        item_id = _item_id(item)

        if item_id in completed:
            continue

        title_fp = _fingerprint(item["title"])
        script_fp = _fingerprint(item["script"])

        if title_fp in uploaded_titles or title_fp in completed_titles:
            print(f"Skipping duplicate title: {item['title']}")
            continue

        if script_fp in completed_scripts:
            print(f"Skipping duplicate script: {item_id}")
            continue

        progress["in_progress"] = {
            "id": item_id,
            "claimed_at": _now(),
        }

        _save(PROGRESS_FILE, progress)

        return item

    return None


def mark_uploaded(item_id, upload_result, item):
    progress = _progress()

    claim = progress.get("in_progress")

    if not claim or claim.get("id") != item_id:
        raise RuntimeError(
            "Only the claimed queue item can be completed"
        )

    progress.setdefault("completed", {})[item_id] = {
        "uploaded_at": _now(),
        "video_id": upload_result.get("video_id"),
        "video_url": upload_result.get("video_url"),
        "title_fingerprint": _fingerprint(item["title"]),
        "script_fingerprint": _fingerprint(item["script"]),
        "visual_fingerprints": [
            _fingerprint(v)
            for v in item["visuals"]
        ],
    }

    progress["in_progress"] = None

    _save(PROGRESS_FILE, progress)


def release_claim(item_id):
    progress = _progress()

    claim = progress.get("in_progress")

    if claim and claim.get("id") == item_id:
        progress["in_progress"] = None
        _save(PROGRESS_FILE, progress)