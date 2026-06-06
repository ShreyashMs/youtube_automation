import json
import os

# ---------------------------------------------------

# PROGRESS FILE

# ---------------------------------------------------

PROGRESS_FILE = "data/series_progress.json"

# ---------------------------------------------------

# LOAD PROGRESS

# ---------------------------------------------------

def load_progress():
    if not os.path.exists(
        PROGRESS_FILE
    ):
        return {}
    with open(
        PROGRESS_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


# ---------------------------------------------------

# SAVE PROGRESS

# ---------------------------------------------------

def save_progress(data):
    os.makedirs(
        "data",
        exist_ok=True
    )
    with open(
        PROGRESS_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


# ---------------------------------------------------

# LOAD JSON

# ---------------------------------------------------

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None


# ---------------------------------------------------

# GET ACTIVE SERIES

# ---------------------------------------------------

def get_active_series():
    try:
        progress_data = load_json("assets/series/series_config.json")
        if progress_data:
            return progress_data.get("active_series", "bhagwat_gita")
    except:
        pass
    return "bhagwat_gita"


# ---------------------------------------------------

# LOAD SERIES

# ---------------------------------------------------

def load_series(series_name):
    try:
        data = load_json(f"assets/series/{series_name}.json")
        return data if data else []
    except:
        return []


# ---------------------------------------------------

# GET NEXT EPISODE

# ---------------------------------------------------

def get_next_episode(series_name=None):
    if not series_name:
        series_name = get_active_series()
    progress = load_progress()
    current_episode = progress.get(
        series_name,
        0
    )
    next_episode_number = (
        current_episode + 1
    )
    data = load_series(series_name)
    for item in data:
        if item.get("episode") == next_episode_number:
            return item
    return None


# ---------------------------------------------------

# MARK EPISODE COMPLETE

# ---------------------------------------------------

def mark_episode_uploaded(
    series_name,
    episode_number
):
    progress = load_progress()
    progress[series_name] = (
        episode_number
    )
    save_progress(progress)

