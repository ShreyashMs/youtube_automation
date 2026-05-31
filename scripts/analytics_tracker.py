import json
import os
from datetime import datetime

# ---------------------------------------------------

# ANALYTICS FILE

# ---------------------------------------------------

ANALYTICS_FILE = "analytics.json"

# ---------------------------------------------------

# LOAD ANALYTICS

# ---------------------------------------------------

def load_analytics():


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


# ---------------------------------------------------

# SAVE ANALYTICS

# ---------------------------------------------------

def save_analytics(data):


with open(
    ANALYTICS_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        data,
        f,
        ensure_ascii=False,
        indent=4
    )


# ---------------------------------------------------

# TRACK VIDEO

# ---------------------------------------------------

def track_video(


topic,
title,
video_id="",
duration=0


):


analytics = load_analytics()

entry = {

    "topic": topic,

    "title": title,

    "video_id": video_id,

    "duration": duration,

    "uploaded_at": str(
        datetime.now()
    )
}

analytics.append(entry)

save_analytics(analytics)

print("\nAnalytics updated")


# ---------------------------------------------------

# GET TOTAL VIDEOS

# ---------------------------------------------------

def get_total_videos():


analytics = load_analytics()

return len(analytics)


# ---------------------------------------------------

# MAIN

# ---------------------------------------------------

if **name** == "**main**":


track_video(

    topic="हनुमानजी अमर क्यों हैं",

    title="हनुमानजी कभी मर क्यों नहीं सकते?"
)

print(
    get_total_videos()
)

