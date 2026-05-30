import os
import requests
import random
import re
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------
# API
# ---------------------------------------------------

API_KEY = os.getenv("PEXELS_API_KEY")

HEADERS = {
    "Authorization": API_KEY
}

DOWNLOAD_FOLDER = "assets/footage"

USED_VIDEO_IDS = set()

# ---------------------------------------------------
# TOPIC → VISUAL QUERIES
# ---------------------------------------------------

VISUAL_MAPPINGS = {

    "शिव": [

        "shiva statue",
        "mahakal temple",
        "himalaya cinematic",
        "ancient temple india",
        "meditation mountain",
        "shivling",
        "lord shiva art",
        "hindu temple cinematic",
    ],

    "राम": [

        "ram mandir",
        "ancient india cinematic",
        "indian temple drone",
        "epic warrior",
        "forest cinematic",
        "indian mythology art",
        "ayodhya temple",
    ],

    "हनुमान": [

        "hanuman statue",
        "epic sky cinematic",
        "indian warrior cinematic",
        "mountain cinematic",
        "sunrise india temple",
        "devotional india",
    ],

    "कृष्ण": [

        "krishna statue",
        "flute cinematic",
        "vrindavan temple",
        "peacock feather",
        "spiritual india",
        "river cinematic",
        "bhagavad gita art",
    ],

    "महाभारत": [

        "epic war",
        "battle cinematic",
        "ancient warriors",
        "indian mythology",
        "battlefield drone",
        "cinematic fire",
    ],

    "रावण": [

        "dark king cinematic",
        "epic fire",
        "ancient warrior",
        "cinematic night",
        "fantasy fort",
    ],

    "शनि": [

        "dark temple",
        "space cinematic",
        "stars cinematic",
        "meditation dark",
        "slow motion temple",
    ],

    "लक्ष्मी": [

        "gold temple",
        "festival india",
        "spiritual woman cinematic",
        "diwali cinematic",
        "wealth aesthetic",
    ]
}

# ---------------------------------------------------
# DEFAULT QUERIES
# ---------------------------------------------------

DEFAULT_QUERIES = [

    "ancient india",
    "cinematic temple",
    "indian spirituality",
    "epic cinematic",
    "indian mythology",
    "hindu temple",
    "spiritual cinematic",
    "india drone",
]

# ---------------------------------------------------
# EXTRACT QUERIES FROM SCRIPT
# ---------------------------------------------------

def get_visual_queries(script_text):

    queries = []

    for keyword, visuals in VISUAL_MAPPINGS.items():

        if keyword in script_text:

            queries.extend(visuals)

    if not queries:

        queries = DEFAULT_QUERIES

    random.shuffle(queries)

    return queries[:5]

# ---------------------------------------------------
# DOWNLOAD VIDEO
# ---------------------------------------------------

def download_video(url, output_path):

    response = requests.get(
        url,
        stream=True,
        timeout=60
    )

    with open(output_path, "wb") as f:

        for chunk in response.iter_content(
            chunk_size=1024 * 1024
        ):

            if chunk:
                f.write(chunk)

# ---------------------------------------------------
# FETCH FOOTAGE
# ---------------------------------------------------

def fetch_footage(script_text):

    print("\nFetching cinematic footage...")

    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    # Clear old clips
    for file in os.listdir(DOWNLOAD_FOLDER):

        path = os.path.join(
            DOWNLOAD_FOLDER,
            file
        )

        if os.path.isfile(path):
            os.remove(path)

    queries = get_visual_queries(
        script_text
    )

    downloaded = 0

    for query in queries:

        try:

            print(f"\nSearching: {query}")

            url = (
                "https://api.pexels.com/videos/search"
                f"?query={query}"
                "&per_page=15"
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

                    USED_VIDEO_IDS.add(video_id)

                    duration = video.get(
                        "duration",
                        0
                    )

                    if duration < 5:
                        continue

                    best_file = None

                    for vf in video.get(
                        "video_files",
                        []
                    ):

                        width = vf.get("width", 0)
                        height = vf.get("height", 0)

                        quality = vf.get(
                            "quality",
                            ""
                        )

                        # Prefer vertical HD
                        if (
                            height > width
                            and height >= 1280
                            and quality == "hd"
                        ):

                            best_file = vf["link"]
                            break

                    # fallback
                    if not best_file:

                        files = video.get(
                            "video_files",
                            []
                        )

                        if files:
                            best_file = files[0]["link"]

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

                    print(
                        f"Saved: {output_path}"
                    )

                    downloaded += 1

                    # enough clips
                    if downloaded >= 7:

                        print(
                            f"\nTotal clips downloaded: {downloaded}"
                        )

                        return

                except Exception as e:

                    print(e)

        except Exception as e:

            print(e)

    print(
        f"\nTotal clips downloaded: {downloaded}"
    )