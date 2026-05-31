import random
import json
import os
from datetime import datetime

USED_TOPICS_FILE = "used_topics.json"

DAY_TOPICS = {

    "Monday": [
        "शिवजी ने विष क्यों पिया",
        "महाकाल का रहस्य",
        "कैलाश पर्वत का रहस्य",
        "नंदी की शक्ति",
        "शिवजी का तीसरा नेत्र",
    ],

    "Tuesday": [
        "हनुमानजी ने सूर्य को क्यों निगला",
        "हनुमानजी अमर क्यों हैं",
        "हनुमानजी और शनिदेव",
        "लंका दहन",
        "संजीवनी बूटी",
    ],

    "Wednesday": [
        "गणेशजी और महाभारत",
        "गणेशजी का टूटा दांत",
        "गणपति बप्पा का रहस्य",
        "गणेशजी और कुबेर",
        "गणेशजी की बुद्धि",
    ],

    "Thursday": [
        "समुद्र मंथन",
        "नरसिंह अवतार",
        "वामन अवतार",
        "गरुड़ की शक्ति",
        "विष्णुजी की माया",
    ],

    "Friday": [
        "मां लक्ष्मी का रहस्य",
        "धनतेरस की कथा",
        "श्री यंत्र का रहस्य",
        "महालक्ष्मी व्रत",
        "दीपावली की कथा",
    ],

    "Saturday": [
        "शनिदेव का न्याय",
        "शनि साढ़ेसाती",
        "शनिदेव और हनुमानजी",
        "शनि मंदिर का रहस्य",
        "शनिदेव का क्रोध",
    ],

    "Sunday": [
        "रामसेतु का रहस्य",
        "रामजी और हनुमानजी",
        "रामराज्य",
        "सूर्यदेव और कर्ण",
        "अयोध्या का रहस्य",
    ]
}

def load_used_topics():

    if not os.path.exists(USED_TOPICS_FILE):
        return []

    try:

        with open(
            USED_TOPICS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:
        return []

def save_used_topic(topic):

    used = load_used_topics()

    used.append(topic)

    used = used[-100:]

    with open(
        USED_TOPICS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            used,
            f,
            ensure_ascii=False,
            indent=2
        )

def get_topic():

    today = datetime.today().strftime("%A")

    if today not in DAY_TOPICS:
        today = "Monday"

    topics = DAY_TOPICS[today]

    used = load_used_topics()

    fresh = [

        t for t in topics
        if t not in used
    ]

    if not fresh:
        fresh = topics

    topic = random.choice(fresh)

    save_used_topic(topic)

    return topic

if __name__ == "__main__":

    print(get_topic())