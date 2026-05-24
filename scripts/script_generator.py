
import requests
import json

PROMPT = """
तुम एक वायरल YouTube Shorts स्क्रिप्ट लेखक हो।

विषय:
महाभारत, रामायण, भारतीय इतिहास, रहस्य

नियम:
नियम:

- पूरी स्क्रिप्ट केवल शुद्ध हिंदी में हो
- एक भी अंग्रेज़ी शब्द नहीं होना चाहिए
- स्क्रिप्ट कम से कम 60 शब्द और अधिकतम 80 शब्द की हो
- स्क्रिप्ट 35 से 45 सेकंड की हो
- पहली पंक्ति बहुत शक्तिशाली और चौंकाने वाली हो
- छोटे और तेज वाक्य लिखो
- रहस्य और जिज्ञासा लगातार बनी रहनी चाहिए
- कहानी पूरी होनी चाहिए
- कहानी बीच में अधूरी नहीं छोड़नी है
- अंत बहुत प्रभावशाली होना चाहिए
- भावनात्मक और नाटकीय शैली रखो
- केवल narration शैली में लिखो
- कोई scene direction नहीं होना चाहिए
- कोई timestamps नहीं होने चाहिए
- किसी भी प्रकार के special characters उपयोग मत करो
- केवल साधारण हिंदी वाक्य लिखो
- उत्तर में किसी प्रकार की व्याख्या मत दो

अंत में यह लाइन ज़रूर लिखो:
"ऐसी और कहानियों के लिए RamLala10 को subscribe करें।"

FORMAT:

HOOK:
...

SCRIPT:
...

CTA:
RamLala10 को subscribe करो।
"""

def generate_script():

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": PROMPT,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]

if __name__ == "__main__":
    print(generate_script())
