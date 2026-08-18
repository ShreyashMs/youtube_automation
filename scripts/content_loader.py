"""Load JSON-authored episodes and persist their execution state.

The series JSON is the content source.  This module deliberately keeps
execution state in ``data/series_progress.json`` instead of editing the
authored JSON files after an upload.
"""

import json
import os
from datetime import datetime, timezone


PROGRESS_FILE = "data/series_progress.json"
SERIES_CONFIG_FILE = "assets/series/series_config.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _save_json_atomic(path, data):
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)
    temporary_path = f"{path}.tmp"
    with open(temporary_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    os.replace(temporary_path, path)


def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {"version": 2, "series": {}}

    data = load_json(PROGRESS_FILE)
    if data.get("version") == 2 and isinstance(data.get("series"), dict):
        return data

    # Migrate the old {"series_name": last_episode_number} format.  The old
    # pointer is retained so completed episode ids can be calculated when the
    # matching series is next loaded.
    legacy = {
        name: number for name, number in data.items()
        if isinstance(number, int)
    }
    return {"version": 2, "series": {}, "legacy_last_episode": legacy}


def save_progress(progress):
    _save_json_atomic(PROGRESS_FILE, progress)


def get_active_series():
    config = load_json(SERIES_CONFIG_FILE)
    return config.get("active_series", "bhagwat_gita")


def get_series_settings(series_name):
    config = load_json(SERIES_CONFIG_FILE)
    settings = config.get("series", {}).get(series_name, {})
    if not settings:
        raise ValueError(f"No JSON settings found for series: {series_name}")
    return settings


def load_series(series_name):
    data = load_json(f"assets/series/{series_name}.json")
    if not isinstance(data, list):
        raise ValueError(f"Series file must contain a JSON array: {series_name}")
    return data


def episode_id(item):
    if item.get("id"):
        return str(item["id"])
    try:
        return f"{item['series']}:chapter-{int(item['chapter'])}:episode-{int(item['episode'])}"
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("Each episode needs id, or series/chapter/episode fields") from error


def _validate_series(items, series_name):
    ids = set()
    for item in items:
        if not isinstance(item, dict):
            raise ValueError(f"{series_name} contains a non-object episode")
        required = ("series", "chapter", "episode", "title", "script", "visual_theme")
        missing = [key for key in required if not item.get(key) and item.get(key) != 0]
        if missing:
            raise ValueError(f"Episode is missing required JSON fields: {', '.join(missing)}")
        item_id = episode_id(item)
        if item_id in ids:
            raise ValueError(f"Duplicate episode id in {series_name}: {item_id}")
        ids.add(item_id)


def _series_progress(progress, series_name, items):
    states = progress.setdefault("series", {})
    state = states.setdefault(series_name, {"completed": {}, "in_progress": None})
    state.setdefault("completed", {})
    state.setdefault("in_progress", None)

    # One-time migration from the legacy sequential counter.
    legacy_number = progress.get("legacy_last_episode", {}).pop(series_name, None)
    if legacy_number is not None:
        for item in items:
            if int(item["episode"]) <= legacy_number:
                state["completed"].setdefault(episode_id(item), {"migrated_at": _utc_now()})
    return state


def _resolve_episode(item, settings):
    defaults = settings.get("defaults", {})
    visual_themes = settings.get("visual_themes", {})
    resolved = dict(item)
    resolved["hashtags"] = item.get("hashtags", defaults.get("hashtags", []))
    resolved["description"] = item.get("description", defaults.get("description", ""))
    resolved["comment"] = item.get("comment", defaults.get("comment", ""))
    resolved["visual_queries"] = item.get(
        "visual_queries",
        visual_themes.get(item["visual_theme"], [])
    )
    if not resolved["visual_queries"]:
        raise ValueError(f"No JSON visual queries for theme: {item['visual_theme']}")
    return resolved


def claim_next_episode(series_name=None):
    """Reserve the next uncompleted item so concurrent runs cannot duplicate it.
    
    If an episode is already in progress, it will be resumed automatically.
    This enables the pipeline to recover from interruptions.
    """
    series_name = series_name or get_active_series()
    settings = get_series_settings(series_name)
    items = load_series(series_name)
    _validate_series(items, series_name)
    items.sort(key=lambda item: (int(item["chapter"]), int(item["episode"])))

    progress = load_progress()
    state = _series_progress(progress, series_name, items)

    active_claim = state.get("in_progress")
    if active_claim:
        # Resume the interrupted episode instead of throwing an error
        in_progress_id = active_claim['episode_id']
        claimed_at = active_claim.get('claimed_at', '')
        
        # Find the episode in the items list
        for item in items:
            if episode_id(item) == in_progress_id:
                print(f"[RESUME] Resuming interrupted episode: {in_progress_id}")
                print(f"[RESUME] Episode was claimed at: {claimed_at}")
                return _resolve_episode(item, settings)
        
        # If the episode is no longer in the series, clear the in_progress marker
        print(f"[WARN] In-progress episode {in_progress_id} not found in series, clearing.")
        state["in_progress"] = None
        save_progress(progress)

    for item in items:
        item_id = episode_id(item)
        if item_id not in state["completed"]:
            state["in_progress"] = {"episode_id": item_id, "claimed_at": _utc_now()}
            save_progress(progress)
            return _resolve_episode(item, settings)

    save_progress(progress)
    return None


def get_next_episode(series_name=None):
    """Backward-compatible alias. New pipelines should use claim_next_episode."""
    return claim_next_episode(series_name)


def mark_episode_uploaded(series_name, episode_number=None, item_id=None, upload_result=None):
    items = load_series(series_name)
    if item_id is None:
        matching = [item for item in items if item.get("episode") == episode_number]
        if len(matching) != 1:
            raise ValueError("Use item_id when episode numbers are not unique")
        item_id = episode_id(matching[0])

    progress = load_progress()
    state = _series_progress(progress, series_name, items)
    claim = state.get("in_progress")
    if claim and claim.get("episode_id") != item_id:
        raise RuntimeError("Cannot complete an episode claimed by another pipeline run")

    state["completed"][item_id] = {
        "completed_at": _utc_now(),
        "video_id": (upload_result or {}).get("video_id"),
        "video_url": (upload_result or {}).get("video_url"),
    }
    state["in_progress"] = None
    save_progress(progress)


def release_episode_claim(series_name, item_id):
    """Release a failed run. Completed episodes are never released."""
    progress = load_progress()
    state = progress.get("series", {}).get(series_name)
    claim = state.get("in_progress") if state else None
    if claim and claim.get("episode_id") == item_id:
        state["in_progress"] = None
        save_progress(progress)
