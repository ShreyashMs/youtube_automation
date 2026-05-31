import random
from datetime import datetime

# ---------------------------------------------------

# CATEGORY TOPICS

# ---------------------------------------------------

TOPIC_CATEGORIES = {


"shiv": [

    "शिवजी ने विष क्यों पिया",
    "महाकाल का रहस्य",
    "कैलाश पर्वत का रहस्य",
    "शिवजी का तांडव",
    "काल भैरव की शक्ति",
    "शिवजी और गंगा",
],

"ram": [

    "रामजी का वनवास",
    "रामसेतु का रहस्य",
    "रामजी और विभीषण",
    "रामराज्य",
    "रामजी और हनुमानजी",
],

"hanuman": [

    "हनुमानजी अमर क्यों हैं",
    "हनुमानजी और शनिदेव",
    "हनुमानजी ने सूर्य को क्यों निगला",
    "हनुमानजी और भीम",
    "हनुमानजी की असली शक्ति",
],

"krishna": [

    "श्रीकृष्ण और सुदामा",
    "गोवर्धन पर्वत का रहस्य",
    "कृष्णजी की बांसुरी",
    "कालिया नाग की कथा",
    "श्रीकृष्ण और अर्जुन",
],

"mahabharat": [

    "कर्ण का सबसे बड़ा रहस्य",
    "भीष्म पितामह का वरदान",
    "द्रौपदी का चीरहरण",
    "अश्वत्थामा अमर क्यों हैं",
    "महाभारत का सबसे बड़ा श्राप",
]


}

# ---------------------------------------------------

# DAY CATEGORY MAP

# ---------------------------------------------------

DAY_MAPPING = {


"Monday": "shiv",
"Tuesday": "hanuman",
"Wednesday": "krishna",
"Thursday": "krishna",
"Friday": "ram",
"Saturday": "hanuman",
"Sunday": "ram"


}

# ---------------------------------------------------

# GET CATEGORY

# ---------------------------------------------------

def get_today_category():


today = datetime.today().strftime("%A")

return DAY_MAPPING.get(
    today,
    "shiv"
)


# ---------------------------------------------------

# GET TOPIC

# ---------------------------------------------------

def get_today_topic():


category = get_today_category()

topics = TOPIC_CATEGORIES.get(
    category,
    []
)

return random.choice(topics)


# ---------------------------------------------------

# GET RANDOM VIRAL TOPIC

# ---------------------------------------------------

def get_random_viral_topic():


all_topics = []

for topics in TOPIC_CATEGORIES.values():

    all_topics.extend(topics)

return random.choice(all_topics)


# ---------------------------------------------------

# MAIN

# ---------------------------------------------------

if **name** == "**main**":


print(get_today_topic())

