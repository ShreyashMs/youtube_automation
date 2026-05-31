import os
import requests
import random
import re
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PEXELS_API_KEY")

HEADERS = {
    "Authorization": API_KEY
}

DOWNLOAD_FOLDER = "assets/footage"

USED_VIDEO_IDS = set()

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

def get_visual_queries(script_text):

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

def fetch_footage(script_text):

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

    queries = get_visual_queries(script_text)

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

                    if video_id in USED_VIDEO_IDS:
                        continue

                    if is_bad_video(video):
                        continue

                    USED_VIDEO_IDS.add(video_id)

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

