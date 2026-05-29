import requests
import random
import re
import time

# ---------------------------------------------------
# TOPICS
# ---------------------------------------------------

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

# ---------------------------------------------------
# INVALID WORDS
# ---------------------------------------------------

BAD_WORDS = [

    "english",
    "follow us",
    "like share",
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
    "lorem",

    # labels
    "hook:",
    "script:",
    "cta:",
    "शीर्षक:",
    "स्क्रिप्ट:",
    "title:",
]

# ---------------------------------------------------
# FACT ERROR DETECTION
# ---------------------------------------------------

FACT_ERRORS = [

    "धृतराष्ट्र की पत्नी कुंती",
    "कर्ण देवताओं के शाप से पैदा हुआ",
    "कृष्ण ने दुर्योधन को वन भेजा",
    "रावण ने स्वर्ग जीत लिया",
]

# ---------------------------------------------------
# CHECK HINDI CONTENT
# ---------------------------------------------------

def is_hindi(text):

    hindi_chars = re.findall(
        r'[\u0900-\u097F]',
        text
    )

    total_chars = re.findall(
        r'[A-Za-z\u0900-\u097F]',
        text
    )

    if len(total_chars) == 0:
        return False

    ratio = len(hindi_chars) / len(total_chars)

    return ratio > 0.92


# ---------------------------------------------------
# CLEAN SCRIPT
# ---------------------------------------------------

def clean_script(script):

    # Remove markdown
    script = script.replace("**", "")

    # Remove labels
    remove_patterns = [

        r'HOOK\s*:',
        r'SCRIPT\s*:',
        r'CTA\s*:',

        r'शीर्षक\s*:',
        r'स्क्रिप्ट\s*:',
        r'वर्णन\s*:',

        r'HOOK',
        r'SCRIPT',
        r'CTA',

        r'शीर्षक',
        r'स्क्रिप्ट',
        r'वर्णन'
    ]

    for pattern in remove_patterns:

        script = re.sub(
            pattern,
            '',
            script,
            flags=re.IGNORECASE
        )

    # Remove extra spaces
    script = script.replace("\n", " ")

    script = re.sub(
        r'\s+',
        ' ',
        script
    )

    # Punctuation cleanup
    script = script.replace(" ,", ",")
    script = script.replace(" ।", "।")
    script = script.replace(" .", ".")
    script = script.replace(" !", "!")
    script = script.replace(" ?", "?")

    return script.strip()


# ---------------------------------------------------
# VALIDATE SCRIPT
# ---------------------------------------------------

def validate_script(script):

    # Bad words
    for word in BAD_WORDS:

        if word.lower() in script.lower():

            print(f"Bad word detected: {word}")

            return False

    # Hindi check
    if not is_hindi(script):

        print("English content detected")

        return False

    # Minimum length
    if len(script) < 220:

        print("Script too short")

        return False

    # Broken narration detection
    bad_patterns = [

        r'निराश,',
        r'क्रोधित,',
        r'भयभीत,',
        r'चौंक गया,',
        r'हार के कगार पर',
        r'युद्ध भयंकर था,',
        r'लालच में फंसा,',
        r'वन में भेजा,',
        r'इतिहास में सबसे',
        r'सबसे बड़ा रहस्य,',
        r'उसके बाद,',
        r'तभी,',
    ]

    for pattern in bad_patterns:

        if re.search(pattern, script):

            print(
                f"Broken narration detected: {pattern}"
            )

            return False

    # Fake mythology detection
    fake_patterns = [

        r'मायावी उद्यान',
        r'गुप्त द्वार',
        r'अमर शक्ति',
        r'दुनिया का सबसे',
        r'किसी को नहीं पता',
        r'इतिहास छुपाता है',
        r'वैज्ञानिक भी हैरान',
    ]

    for pattern in fake_patterns:

        if re.search(pattern, script):

            print(
                f"Possible fake content: {pattern}"
            )

            return False

    # Fact validation
    for error in FACT_ERRORS:

        if error in script:

            print(
                f"Fact error detected: {error}"
            )

            return False

    return True


# ---------------------------------------------------
# GENERATE SCRIPT
# ---------------------------------------------------

def generate_script():

    topic = random.choice(TOPICS)

    print(f"\nGenerating topic: {topic}")

    PROMPT = f"""
तुम भारतीय पौराणिक कथाओं के विशेषज्ञ और YouTube Shorts के पेशेवर लेखक हो।

तुम्हारा काम केवल तथ्य आधारित, प्राकृतिक और भावनात्मक narration लिखना है।

विषय:
{topic}

सख्त नियम:

- पूरी स्क्रिप्ट केवल शुद्ध हिंदी में हो
- एक भी अंग्रेज़ी शब्द नहीं होना चाहिए
- सभी तथ्य पौराणिक ग्रंथों के अनुसार सही होने चाहिए
- कोई fake story या काल्पनिक घटना मत जोड़ो
- किसी पात्र के बारे में गलत जानकारी मत लिखो
- narration ऐसा लगे जैसे इंसान कहानी सुना रहा हो
- हर वाक्य पूरा और प्राकृतिक होना चाहिए
- अधूरे cinematic वाक्य बिल्कुल नहीं लिखने
- commas से टूटे हुए वाक्य मत लिखो
- छोटे लेकिन स्पष्ट वाक्य लिखो
- hook बहुत शक्तिशाली होना चाहिए
- suspense लगातार बना रहना चाहिए
- अंत emotional और impactful होना चाहिए
- स्क्रिप्ट लगभग 100 शब्द की हो
- कोई headings नहीं
- कोई labels नहीं
- HOOK नहीं लिखना
- SCRIPT नहीं लिखना
- CTA नहीं लिखना
- शीर्षक नहीं लिखना
- emojis नहीं
- special characters नहीं

महत्वपूर्ण:

यह स्क्रिप्ट Text To Speech आवाज़ में बोली जाएगी।

इसलिए हर वाक्य बोलने में साफ़, प्राकृतिक और सहज होना चाहिए।

गलत उदाहरण:
अर्जुन निराश, पाण्डव हार के कगार पर।

सही उदाहरण:
अर्जुन निराश थे और पाण्डव हार के कगार पर पहुँच चुके थे।

स्क्रिप्ट के अंत में केवल यह पंक्ति जोड़ो:

ऐसी और कहानियों के लिए रामलला१० को Subscribe करो, आपका दिन शुभ जाएगा और आपकी परेशानी दूर हो जाएगी।
"""

    try:

        response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model": "gemma3:12b",

                "prompt": PROMPT,

                "stream": False,

                "options": {

                    "temperature": 0.65,
                    "top_p": 0.9,
                    "repeat_penalty": 1.15,
                    "num_predict": 250
                }
            },

            timeout=120
        )

        data = response.json()

        raw_script = data["response"].strip()

        script = clean_script(raw_script)

        # Validate script
        if not validate_script(script):

            print(
                "\nInvalid script detected. Regenerating...\n"
            )

            time.sleep(1)

            return generate_script()

        # Save script
        with open(
            "script.txt",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(script)

        print("\nFINAL SCRIPT:\n")

        print(script)

        return script

    except Exception as e:

        print("\nError generating script:")
        print(e)

        print("\nRetrying...\n")

        time.sleep(2)

        return generate_script()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":

    print(generate_script())
