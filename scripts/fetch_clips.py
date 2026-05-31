import os
import requests
import random
from dotenv import load_dotenv

# ---------------------------------------------------
# LOAD ENV
# ---------------------------------------------------

load_dotenv()

API_KEY = os.getenv("PEXELS_API_KEY")

# ---------------------------------------------------
# VALIDATE API KEY
# ---------------------------------------------------

if not API_KEY:

    raise Exception(
        "PEXELS_API_KEY not found in .env"
    )

# ---------------------------------------------------
# HEADERS
# ---------------------------------------------------

HEADERS = {

    "Authorization": API_KEY
}

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

SEARCH_QUERY = "ancient battle"

PER_PAGE = 10

MIN_DURATION = 5

# ---------------------------------------------------
# SEARCH VIDEOS
# ---------------------------------------------------

def fetch_clips(

    query=SEARCH_QUERY,

    per_page=PER_PAGE
):

    print(
        f"\nSearching Pexels for: {query}"
    )

    url = (

        "https://api.pexels.com/videos/search"

        f"?query={query}"

        f"&per_page={per_page}"
    )

    try:

        response = requests.get(

            url,

            headers=HEADERS,

            timeout=30
        )

        # ---------------------------------------------------
        # API CHECK
        # ---------------------------------------------------

        if response.status_code != 200:

            raise Exception(

                f"Pexels API Error: "
                f"{response.status_code}"
            )

        data = response.json()

        videos = data.get(
            "videos",
            []
        )

        if not videos:

            print("\nNo videos found")

            return []

        print(
            f"\nFound {len(videos)} videos"
        )

        valid_videos = []

        # ---------------------------------------------------
        # FILTER VIDEOS
        # ---------------------------------------------------

        for video in videos:

            try:

                video_id = video.get("id")

                duration = video.get(
                    "duration",
                    0
                )

                if duration < MIN_DURATION:

                    continue

                best_file = None

                for vf in video.get(
                    "video_files",
                    []
                ):

                    width = vf.get(
                        "width",
                        0
                    )

                    height = vf.get(
                        "height",
                        0
                    )

                    quality = vf.get(
                        "quality",
                        ""
                    )

                    # prefer vertical HD
                    if (

                        height > width

                        and height >= 1280

                        and quality == "hd"
                    ):

                        best_file = vf

                        break

                # fallback
                if not best_file:

                    files = video.get(
                        "video_files",
                        []
                    )

                    if files:

                        best_file = files[0]

                if not best_file:

                    continue

                clip_data = {

                    "id": video_id,

                    "duration": duration,

                    "width": best_file.get(
                        "width"
                    ),

                    "height": best_file.get(
                        "height"
                    ),

                    "quality": best_file.get(
                        "quality"
                    ),

                    "link": best_file.get(
                        "link"
                    )
                }

                valid_videos.append(
                    clip_data
                )

            except Exception as e:

                print(e)

        # ---------------------------------------------------
        # RANDOMIZE RESULTS
        # ---------------------------------------------------

        random.shuffle(valid_videos)

        return valid_videos

    except Exception as e:

        print("\nERROR:")
        print(e)

        return []

# ---------------------------------------------------
# TEST
# ---------------------------------------------------

if __name__ == "__main__":

    clips = fetch_clips()

    print("\nRESULTS:\n")

    for index, clip in enumerate(

        clips[:5],

        start=1
    ):

        print(f"Clip {index}")

        print(
            f"ID: {clip['id']}"
        )

        print(
            f"Duration: "
            f"{clip['duration']} sec"
        )

        print(
            f"Resolution: "
            f"{clip['width']}x{clip['height']}"
        )

        print(
            f"Quality: "
            f"{clip['quality']}"
        )

        print(
            f"Link: "
            f"{clip['link'][:80]}..."
        )

        print("-" * 50)