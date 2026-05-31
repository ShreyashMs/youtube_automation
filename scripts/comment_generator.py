import requests
import re

# ---------------------------------------------------
# CLEAN TEXT
# ---------------------------------------------------

def clean_text(text):

    text = text.replace("**", "")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()

# ---------------------------------------------------
# GENERATE COMMENT
# ---------------------------------------------------

def generate_comment(script):

    prompt = f"""
तुम YouTube Shorts engagement expert हो।

नीचे दिए गए devotional script के लिए:

1. एक emotional Hindi comment लिखो
2. comment ऐसा हो कि लोग like और reply करें
3. भगवान का आशीर्वाद वाला tone हो
4. comment 2 से 4 lines का हो
5. channel subscribe करने के लिए naturally बोलो
6. emoji बहुत कम use करो
7. comment realistic लगे
8. कोई quotes नहीं
9. सिर्फ comment output करो

SCRIPT:
{script}
"""

    try:

        response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model": "gemma3:12b",

                "prompt": prompt,

                "stream": False,

                "options": {

                    "temperature": 0.9,
                    "top_p": 0.95,
                    "repeat_penalty": 1.1,
                    "num_predict": 120
                }
            },

            timeout=120
        )

        comment = response.json().get(
            "response",
            ""
        )

        comment = clean_text(comment)

        if len(comment) < 10:

            return (
                "जय श्री राम 🙏\n"
                "भगवान आपकी सभी परेशानियाँ दूर करें।\n"
                "ऐसी और दिव्य कथाओं के लिए चैनल को Subscribe करें।"
            )

        return comment

    except Exception as e:

        print(f"\nComment generation error: {e}")

        return (
            "जय श्री राम 🙏\n"
            "भगवान आपकी सभी परेशानियाँ दूर करें।\n"
            "ऐसी और दिव्य कथाओं के लिए चैनल को Subscribe करें।"
        )


# ---------------------------------------------------
# TEST
# ---------------------------------------------------

if __name__ == "__main__":

    sample_script = '''
    हनुमानजी ने सूर्यदेव को फल समझकर निगल लिया था।
    '''

    print(generate_comment(sample_script))

