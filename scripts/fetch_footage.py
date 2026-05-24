import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PEXELS_API_KEY")

HEADERS = {
    "Authorization": API_KEY
}

DOWNLOAD_FOLDER = "assets/footage"


def fetch_footage(query="ancient india", per_page=5):

    print(f"\nSearching footage for: {query}")

    # Create folder if not exists
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    url = (
        f"https://api.pexels.com/videos/search"
        f"?query={query}&per_page={per_page}"
    )

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print("Failed to fetch footage")
        print(response.text)
        return

    data = response.json()

    videos = data.get("videos", [])

    if not videos:
        print("No footage found.")
        return

    # Clear old clips
    for file in os.listdir(DOWNLOAD_FOLDER):

        file_path = os.path.join(DOWNLOAD_FOLDER, file)

        if os.path.isfile(file_path):
            os.remove(file_path)

    downloaded = 0

    for i, video in enumerate(videos):

        try:

            video_files = video.get("video_files", [])

            best_file = None

            # Prefer vertical videos
            for vf in video_files:

                width = vf.get("width", 0)
                height = vf.get("height", 0)

                if height > width:

                    best_file = vf["link"]
                    break

            # Fallback to first available
            if not best_file and video_files:
                best_file = video_files[0]["link"]

            if not best_file:
                continue

            output_path = f"{DOWNLOAD_FOLDER}/clip{i+1}.mp4"

            print(f"Downloading clip {i+1}...")

            video_response = requests.get(
                best_file,
                stream=True,
                timeout=30
            )

            with open(output_path, "wb") as f:

                for chunk in video_response.iter_content(
                    chunk_size=1024
                ):

                    if chunk:
                        f.write(chunk)

            print(f"Downloaded: {output_path}")

            downloaded += 1

        except Exception as e:

            print(f"Failed downloading clip {i+1}")
            print(e)

    print(f"\nTotal clips downloaded: {downloaded}")


if __name__ == "__main__":

    fetch_footage("ancient temple")