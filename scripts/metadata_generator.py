import requests
import re

def generate_metadata(script):

    prompt = f"""
तुम एक वायरल YouTube SEO विशेषज्ञ हो।

नीचे दिए गए narration के लिए:

1. एक बहुत वायरल हिंदी title लिखो
2. SEO friendly description लिखो
3. 10 trending hashtags लिखो

नियम:

- title छोटा और शक्तिशाली हो
- title में curiosity हो
- description 2-3 lines की हो
- hashtags हिंदी और english दोनों में हों
- कोई explanation मत दो

SCRIPT:
{script}

FORMAT:

TITLE:
...

DESCRIPTION:
...

HASHTAGS:
...
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()["response"]

    title = re.search(
        r"TITLE:\s*(.*?)\s*DESCRIPTION:",
        data,
        re.DOTALL
    )

    description = re.search(
        r"DESCRIPTION:\s*(.*?)\s*HASHTAGS:",
        data,
        re.DOTALL
    )

    hashtags = re.search(
        r"HASHTAGS:\s*(.*)",
        data,
        re.DOTALL
    )

    return {
        "title": title.group(1).strip() if title else "",
        "description": description.group(1).strip() if description else "",
        "hashtags": hashtags.group(1).strip() if hashtags else ""
    }