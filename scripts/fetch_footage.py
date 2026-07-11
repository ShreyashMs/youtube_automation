import os
import requests
import random
import re
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PEXELS_API_KEY")

HEADERS = {
    "Authorization": API_KEY
}

DOWNLOAD_FOLDER = "assets/footage"
USED_FOOTAGE_FILE = "data/used_footage.json"

USED_VIDEO_IDS = set()


def load_used_video_ids():
    if not os.path.exists(USED_FOOTAGE_FILE):
        return set()
    try:
        with open(USED_FOOTAGE_FILE, "r", encoding="utf-8") as file:
            return set(json.load(file).get("video_ids", []))
    except (OSError, ValueError, TypeError):
        return set()


def save_used_video_ids(video_ids):
    os.makedirs(os.path.dirname(USED_FOOTAGE_FILE), exist_ok=True)
    temporary_path = f"{USED_FOOTAGE_FILE}.tmp"
    with open(temporary_path, "w", encoding="utf-8") as file:
        json.dump({"video_ids": sorted(video_ids)}, file, indent=2)
    os.replace(temporary_path, USED_FOOTAGE_FILE)

# ---------------------------------------------------
# VISUAL MAPPINGS
# ---------------------------------------------------

VISUAL_MAPPINGS = {

    "शिव": [
        "shiva statue cinematic",
        "mahakal temple drone",
        "shivling close up",
        "himalaya cinematic",
        "dark temple cinematic",
    ],

    "राम": [
        "ram mandir drone",
        "ancient india cinematic",
        "epic warrior silhouette",
        "forest cinematic",
        "ayodhya temple",
    ],

    "हनुमान": [
        "hanuman statue cinematic",
        "epic sky cinematic",
        "mountain cinematic",
        "fire cinematic",
        "strength cinematic",
    ],

    "कृष्ण": [
        "krishna statue cinematic",
        "flute cinematic",
        "vrindavan temple",
        "river cinematic",
        "peacock feather macro",
    ],

    "महाभारत": [
        "epic war cinematic",
        "battlefield drone",
        "ancient warriors",
        "war smoke cinematic",
    ],
    "कर्ण": [
    "epic warrior cinematic",
    "sunrise warrior",
    "ancient battlefield",
    "royal warrior armor",
    ],

    "अर्जुन": [
        "archer cinematic",
        "warrior with bow",
        "battlefield cinematic",
        "epic arrow slow motion",
    ],

    "भीष्म": [
        "old warrior cinematic",
        "epic battlefield",
        "ancient india war",
        "warrior meditation",
    ],

    "द्रौपदी": [
        "queen cinematic",
        "ancient palace india",
        "royal woman silhouette",
        "epic palace cinematic",
    ],

    "अभिमन्यु": [
        "young warrior cinematic",
        "battlefield smoke",
        "epic warrior",
        "war cinematic",
    ],

    "परशुराम": [
        "axe warrior cinematic",
        "forest warrior",
        "epic sage cinematic",
        "ancient warrior",
    ],

    "रावण": [
        "dark king cinematic",
        "fire cinematic",
        "epic villain",
        "dark temple cinematic",
    ],
}

DEFAULT_QUERIES = [

    "ancient india cinematic",
    "hindu temple drone",
    "epic cinematic",
    "spiritual india",
    "mythology cinematic",
]

BAD_KEYWORDS = [

    "wedding",
    "dance",
    "fashion",
    "food",
    "party",
    "travel vlog",
]

# ---------------------------------------------------
# CLEAN QUERY
# ---------------------------------------------------

def clean_query(query):

    query = query.strip().lower()

    query = re.sub(
        r"\s+",
        " ",
        query
    )

    return query

# ---------------------------------------------------
# GET VISUAL QUERIES
# ---------------------------------------------------

def get_visual_queries(script_text, visual_queries=None):
    # JSON-supplied prompts take priority. They are intentionally not inferred
    # from the narration, so the content creator controls every visual intent.
    if visual_queries:
        queries = [clean_query(str(query)) for query in visual_queries if str(query).strip()]
        if not queries:
            raise ValueError("visual_queries must contain at least one non-empty query")
        return list(dict.fromkeys(queries))


    queries = []

    script_text = script_text.lower()

    for keyword, visuals in VISUAL_MAPPINGS.items():

        if keyword.lower() in script_text:

            queries.extend(visuals)

    if not queries:
        queries = DEFAULT_QUERIES.copy()

    queries.extend(DEFAULT_QUERIES)

    queries = list(set(queries))

    random.shuffle(queries)

    return queries[:8]

# ---------------------------------------------------
# FILTER BAD VIDEOS
# ---------------------------------------------------

def is_bad_video(video):

    try:

        user = str(
            video.get("user", {})
            .get("name", "")
        ).lower()

        url = str(
            video.get("url", "")
        ).lower()

        combined = f"{user} {url}"

        for word in BAD_KEYWORDS:

            if word in combined:
                return True

        return False

    except:
        return False

# ---------------------------------------------------
# DOWNLOAD VIDEO
# ---------------------------------------------------

def download_video(url, output_path):

    response = requests.get(
        url,
        stream=True,
        timeout=120
    )

    with open(output_path, "wb") as f:

        for chunk in response.iter_content(
            chunk_size=1024 * 1024
        ):

            if chunk:
                f.write(chunk)

# ---------------------------------------------------
# GET BEST FILE
# ---------------------------------------------------

def get_best_video_file(video_files):

    vertical_hd = []
    vertical = []
    horizontal_hd = []

    for vf in video_files:

        width = vf.get("width", 0)
        height = vf.get("height", 0)

        quality = vf.get("quality", "")

        link = vf.get("link")

        if not link:
            continue

        ratio = height / max(width, 1)

        if ratio >= 1.6:

            if height >= 1280 and quality == "hd":
                vertical_hd.append(vf)
            else:
                vertical.append(vf)

        elif quality == "hd":

            horizontal_hd.append(vf)

    for collection in [

        vertical_hd,
        vertical,
        horizontal_hd

    ]:

        if collection:

            collection.sort(
                key=lambda x: x.get("height", 0),
                reverse=True
            )

            return collection[0]["link"]

    return None

# ---------------------------------------------------
# FETCH FOOTAGE
# ---------------------------------------------------

def fetch_footage(script_text, visual_queries=None):

    print("\nFetching cinematic footage...")

    os.makedirs(
        DOWNLOAD_FOLDER,
        exist_ok=True
    )

    for file in os.listdir(DOWNLOAD_FOLDER):

        path = os.path.join(
            DOWNLOAD_FOLDER,
            file
        )

        if os.path.isfile(path):
            os.remove(path)

    queries = get_visual_queries(script_text, visual_queries)
    used_video_ids = load_used_video_ids() | USED_VIDEO_IDS

    downloaded = 0

    for query in queries:

        try:

            query = clean_query(query)

            print(f"\nSearching: {query}")

            url = (
                "https://api.pexels.com/videos/search"
                f"?query={query}"
                "&per_page=20"
                "&orientation=portrait"
            )

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=30
            )

            if response.status_code != 200:
                continue

            data = response.json()

            videos = data.get("videos", [])

            random.shuffle(videos)

            for video in videos:

                try:

                    video_id = video.get("id")

                    if video_id in used_video_ids:
                        continue

                    if is_bad_video(video):
                        continue

                    duration = video.get(
                        "duration",
                        0
                    )

                    if duration < 5 or duration > 25:
                        continue

                    best_file = get_best_video_file(
                        video.get(
                            "video_files",
                            []
                        )
                    )

                    if not best_file:
                        continue

                    output_path = (
                        f"{DOWNLOAD_FOLDER}/clip{downloaded+1}.mp4"
                    )

                    print(
                        f"Downloading clip {downloaded+1}"
                    )

                    download_video(
                        best_file,
                        output_path
                    )

                    downloaded += 1
                    used_video_ids.add(video_id)
                    USED_VIDEO_IDS.add(video_id)
                    save_used_video_ids(used_video_ids)

                    if downloaded >= 8:

                        print(
                            f"\nTotal clips downloaded: {downloaded}"
                        )

                        return downloaded

                except Exception as e:

                    print(e)

        except Exception as e:

            print(e)

    print(
        f"\nTotal clips downloaded: {downloaded}"
    )

    return downloaded
