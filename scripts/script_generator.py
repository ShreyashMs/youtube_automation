import requests
import random
import re

TOPICS = [

    "अश्वत्थामा का श्राप",

    "कर्ण का सबसे बड़ा रहस्य",

    "भीष्म पितामह की मृत्यु",

    "रावण की असली शक्ति",

    "हनुमान और भीम की मुलाकात",

    "कृष्ण की गुप्त नीति",

    "महाभारत का सबसे खतरनाक योद्धा",

    "द्रोणाचार्य का रहस्य",

    "राम से जुड़ा रहस्य",

    "शिव का प्राचीन मंदिर",

    "चाणक्य की गुप्त योजना",

    "भारत का खोया हुआ शहर",

    "समुद्र मंथन का रहस्य",

    "कलियुग की भविष्यवाणी",

    "विष्णु के गुप्त अवतार"
]

BAD_WORDS = [
    "english",
    "subscribe to",
    "mythological",
    "journey",
    "cultural heritage",
    "ashwatthama",
    "mahabharata",
    "ramayana",
    "krishna",
    "shiva",
    "unknown",
    "asdf",
    "lorem"
]


def is_hindi(text):

    hindi_chars = re.findall(r'[\u0900-\u097F]', text)

    total_chars = re.findall(r'[A-Za-z\u0900-\u097F]', text)

    if len(total_chars) == 0:
        return False

    ratio = len(hindi_chars) / len(total_chars)

    return ratio > 0.85


def generate_script():

    topic = random.choice(TOPICS)

    print(f"\nGenerating topic: {topic}")

    PROMPT = f"""
तुम भारतीय पौराणिक कथाओं के विशेषज्ञ और वायरल YouTube Shorts लेखक हो।

तुम्हारा काम केवल तथ्य आधारित और भावनात्मक कहानी लिखना है।

विषय:
{topic}

महत्वपूर्ण नियम:

- पूरी स्क्रिप्ट केवल हिंदी में हो
- एक भी अंग्रेज़ी शब्द नहीं होना चाहिए
- कहानी केवल इसी विषय पर आधारित हो
- कहानी पूरी तरह समझ में आनी चाहिए
- कहानी शुरुआत से अंत तक connected हो
- कोई गलत तथ्य नहीं
- कोई काल्पनिक जानकारी मत जोड़ो
- छोटे और तेज वाक्य लिखो
- hook बहुत शक्तिशाली हो
- suspense लगातार बना रहना चाहिए
- narration cinematic हो
- अंत emotional और shocking हो
- script लगभग 90 शब्द की हो
- कोई headings नहीं
- कोई explanation नहीं
- कोई emojis नहीं
- कोई special characters नहीं

उत्तर का FORMAT बिल्कुल ऐसा होना चाहिए:

HOOK:
एक छोटी शक्तिशाली पंक्ति

SCRIPT:
पूरा narration

CTA:
ऐसी और कहानियों के लिए RamLala10 को subscribe करें।
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3:12b",
            "prompt": PROMPT,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "repeat_penalty": 1.2
            }
        }
    )

    data = response.json()

    script = data["response"].strip()

    # REMOVE EXTRA MARKDOWN
    script = script.replace("**", "")

    # VALIDATION

    invalid = False

    # Check bad english words
    for word in BAD_WORDS:

        if word.lower() in script.lower():
            invalid = True
            print(f"Bad word detected: {word}")
            break

    # Check mostly Hindi
    if not is_hindi(script):
        invalid = True
        print("English content detected")

    # Check required sections
    if "HOOK:" not in script:
        invalid = True

    if "SCRIPT:" not in script:
        invalid = True

    if "CTA:" not in script:
        invalid = True

    # Too short
    if len(script) < 150:
        invalid = True

    # Regenerate if invalid
    if invalid:

        print("\nInvalid script detected. Regenerating...\n")

        return generate_script()

    return script


if __name__ == "__main__":

    print(generate_script())