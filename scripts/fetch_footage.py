import os
import requests
import random
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PEXELS_API_KEY")

HEADERS = {
    "Authorization": API_KEY
}

DOWNLOAD_FOLDER = "assets/footage"

USED_VIDEO_IDS = set()


def fetch_footage(query="ancient india", per_page=10):

    print(f"\nSearching footage for: {query}")

    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    # Clear old clips
    for file in os.listdir(DOWNLOAD_FOLDER):

        file_path = os.path.join(DOWNLOAD_FOLDER, file)

        if os.path.isfile(file_path):
            os.remove(file_path)

    url = (
        f"https://api.pexels.com/videos/search"
        f"?query={query}"
        f"&per_page={per_page}"
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    if response.status_code != 200:

        print("Failed to fetch footage")
        print(response.text)
        return

    data = response.json()

    videos = data.get("videos", [])

    if not videos:

        print("No footage found.")
        return

    random.shuffle(videos)

    downloaded = 0

    for video in videos:

        try:

            video_id = video.get("id")

            # Avoid duplicates
            if video_id in USED_VIDEO_IDS:
                continue

            USED_VIDEO_IDS.add(video_id)

            duration = video.get("duration", 0)

            # Skip very short clips
            if duration < 5:
                continue

            video_files = video.get("video_files", [])

            best_file = None

            for vf in video_files:

                width = vf.get("width", 0)
                height = vf.get("height", 0)

                quality = vf.get("quality", "")

                # Prefer HD vertical clips
                if (
                    height > width and
                    height >= 1280 and
                    quality == "hd"
                ):

                    best_file = vf["link"]
                    break

            # fallback
            if not best_file and video_files:
                best_file = video_files[0]["link"]

            if not best_file:
                continue

            output_path = (
                f"{DOWNLOAD_FOLDER}/clip{downloaded+1}.mp4"
            )

            print(
                f"Downloading clip {downloaded+1}..."
            )

            video_response = requests.get(
                best_file,
                stream=True,
                timeout=60
            )

            with open(output_path, "wb") as f:

                for chunk in video_response.iter_content(
                    chunk_size=1024 * 1024
                ):

                    if chunk:
                        f.write(chunk)

            print(f"Downloaded: {output_path}")

            downloaded += 1

            # Stop after 5 clips
            if downloaded >= 5:
                break

        except Exception as e:

            print("Download failed")
            print(e)

    print(
        f"\nTotal clips downloaded: {downloaded}"
    )