import requests
import random
import re
import time
import json
import os

from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:12b"

SCRIPT_FILE = "script.txt"
USED_TOPICS_FILE = "used_topics.json"

HOOK_STYLES = [

    "क्या आप जानते हैं",
    "बहुत कम लोग जानते हैं",
    "यह रहस्य आज भी लोगों को चौंका देता है",
    "इस घटना ने पूरे इतिहास को बदल दिया",
]

TOPICS = [

    "हनुमानजी ने सूर्य को क्यों निगला",
    "शिवजी का तीसरा नेत्र",
    "कर्ण का सबसे बड़ा रहस्य",
    "रामसेतु का रहस्य",
    "महाभारत का सबसे शक्तिशाली योद्धा",
    "श्रीकृष्ण की गुप्त नीति",
]

def clean_script(script):

    script = script.replace("**", "")

    script = re.sub(
        r'\s+',
        ' ',
        script
    )

    return script.strip()

def validate_script(script):

    if len(script) < 250:
        return False

    hindi_chars = re.findall(
        r'[\u0900-\u097F]',
        script
    )

    if len(hindi_chars) < 80:
        return False

    return True

def build_prompt(topic):

    hook = random.choice(HOOK_STYLES)

    return f"""
तुम भारत के सर्वश्रेष्ठ पौराणिक कथाकार हो।

विषय:
{topic}

शुरुआत इस प्रकार करो:
{hook}

नियम:

- पूरी स्क्रिप्ट शुद्ध हिंदी में हो
- cinematic narration हो
- suspense बना रहे
- narration voiceover जैसा लगे
- fake बातें मत लिखो
- emojis मत लिखो
- hashtags मत लिखो
- headings मत लिखो
- 120 से 150 शब्द लिखो

अंत में यह पंक्ति जोड़ो:

ऐसी और दिव्य कथाओं के लिए रामलला१० को Subscribe करो। जय श्री राम।
"""

def generate_script():

    topic = random.choice(TOPICS)

    print(f"\nGenerating topic: {topic}")

    prompt = build_prompt(topic)

    try:

        response = requests.post(

            OLLAMA_URL,

            json={

                "model": MODEL_NAME,

                "prompt": prompt,

                "stream": False,

                "options": {

                    "temperature": 0.85,
                    "top_p": 0.9,
                    "repeat_penalty": 1.15,
                    "num_predict": 320,
                }
            },

            timeout=180
        )

        data = response.json()

        raw_script = data.get(
            "response",
            ""
        ).strip()

        script = clean_script(raw_script)

        if not validate_script(script):

            print("\nInvalid script. Retrying...\n")

            time.sleep(2)

            return generate_script()

        with open(
            SCRIPT_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(script)

        return script

    except Exception as e:

        print(e)

        time.sleep(3)

        return generate_script()

if __name__ == "__main__":

    print(generate_script())

