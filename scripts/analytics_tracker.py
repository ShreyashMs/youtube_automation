import json
import os
from datetime import datetime

ANALYTICS_FILE = "analytics.json"

def load_data():

    if not os.path.exists(
        ANALYTICS_FILE
    ):

        return []

    try:

        with open(
            ANALYTICS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:
        return []

def save_video_data(

    title,

    topic,

    video_id,

    video_url
):

    data = load_data()

    entry = {

        "title": title,

        "topic": topic,

        "video_id": video_id,

        "video_url": video_url,

        "uploaded_at": str(
            datetime.now()
        )
    }

    data.append(entry)

    with open(
        ANALYTICS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(
        "\nAnalytics saved successfully"
    )

if __name__ == "__main__":

    save_video_data(

        "हनुमानजी की शक्ति",

        "हनुमान",

        "abc123",

        "https://youtube.com/shorts/abc123"
    )