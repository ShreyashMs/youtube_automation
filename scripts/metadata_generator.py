import requests
import re
import random

# ---------------------------------------------------
# FALLBACK HASHTAGS
# ---------------------------------------------------

DEFAULT_HASHTAGS = [

    "#महाभारत",
    "#रामायण",
    "#हनुमान",
    "#शिव",
    "#HinduMythology",
    "#IndianMythology",
    "#Mythology",
    "#Shorts",
    "#YouTubeShorts",
    "#RamLala10",
]

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
# EXTRACT KEYWORDS
# ---------------------------------------------------

def extract_keywords(script):

    keywords = []

    mappings = {

        "हनुमान": [
            "#हनुमान",
            "#Hanuman",
            "#Bajrangbali",
            "#HanumanJi",
        ],

        "राम": [
            "#राम",
            "#Ram",
            "#Ramayana",
            "#JaiShriRam",
        ],

        "कृष्ण": [
            "#कृष्ण",
            "#Krishna",
            "#Mahabharat",
            "#BhagavadGita",
        ],

        "शिव": [
            "#शिव",
            "#Mahadev",
            "#Shiv",
            "#Bholenath",
        ],

        "रावण": [
            "#Ravan",
            "#Ravana",
            "#Ramayan",
        ],

        "महाभारत": [
            "#Mahabharat",
            "#Mahabharata",
            "#Kurukshetra",
        ],

        "दुर्गा": [
            "#Durga",
            "#MaaDurga",
            "#Navratri",
        ],

        "शनि": [
            "#ShaniDev",
            "#Shani",
            "#शनिदेव",
        ],
    }

    for key, values in mappings.items():

        if key in script:

            keywords.extend(values)

    return list(set(keywords))

# ---------------------------------------------------
# CLEAN TITLE
# ---------------------------------------------------

def clean_title(title):

    title = clean_text(title)

    # remove quotes
    title = title.replace('"', "")
    title = title.replace("“", "")
    title = title.replace("”", "")

    # remove labels
    bad_patterns = [

        r"TITLE\s*:",
        r"DESCRIPTION\s*:",
        r"HASHTAGS\s*:",
    ]

    for pattern in bad_patterns:

        title = re.sub(
            pattern,
            "",
            title,
            flags=re.IGNORECASE
        )

    # Keep title punchy
    if len(title) > 95:
        title = title[:95].strip()

    return title

# ---------------------------------------------------
# CLEAN DESCRIPTION
# ---------------------------------------------------

def clean_description(description):

    description = clean_text(description)

    # remove extra hashtags from description
    description = re.sub(
        r"#\S+",
        "",
        description
    )

    description = description.strip()

    return description

# ---------------------------------------------------
# CLEAN HASHTAGS
# ---------------------------------------------------

def clean_hashtags(text):

    hashtags = re.findall(
        r"#\w+",
        text
    )

    hashtags = list(dict.fromkeys(hashtags))

    return hashtags[:10]

# ---------------------------------------------------
# GENERATE METADATA
# ---------------------------------------------------

def generate_metadata(script):

    keyword_tags = extract_keywords(script)

    prompt = f"""
तुम YouTube Shorts के लिए viral metadata expert हो।

नीचे दिए गए narration के लिए:

1. बहुत वायरल हिंदी title लिखो
2. emotional + curiosity based title हो
3. title 45 से 75 characters के बीच हो
4. SEO friendly description लिखो
5. 10 viral hashtags लिखो

IMPORTANT RULES:

- title में shock, mystery, emotion या secret angle हो
- बहुत लंबे title मत लिखो
- कोई emoji नहीं
- कोई explanation नहीं
- hashtags सिर्फ एक लाइन में लिखो
- hashtags में Hindi + English mix होना चाहिए
- description 2 छोटी lines की हो
- चैनल नाम RamLala10 जरूर mention करो

SCRIPT:
{script}

OUTPUT FORMAT:

TITLE:
...

DESCRIPTION:
...

HASHTAGS:
...
"""

    try:

        response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model": "gemma3:12b",

                "prompt": prompt,

                "stream": False,

                "options": {

                    "temperature": 0.8,
                    "top_p": 0.9,
                    "repeat_penalty": 1.15,
                    "num_predict": 220
                }
            },

            timeout=120
        )

        raw_data = response.json().get(
            "response",
            ""
        )

        # ---------------------------------------------------
        # PARSE
        # ---------------------------------------------------

        title_match = re.search(

            r"TITLE:\s*(.*?)\s*DESCRIPTION:",

            raw_data,

            re.DOTALL | re.IGNORECASE
        )

        description_match = re.search(

            r"DESCRIPTION:\s*(.*?)\s*HASHTAGS:",

            raw_data,

            re.DOTALL | re.IGNORECASE
        )

        hashtags_match = re.search(

            r"HASHTAGS:\s*(.*)",

            raw_data,

            re.DOTALL | re.IGNORECASE
        )

        title = clean_title(

            title_match.group(1)
            if title_match else
            ""
        )

        description = clean_description(

            description_match.group(1)
            if description_match else
            ""
        )

        hashtags = clean_hashtags(

            hashtags_match.group(1)
            if hashtags_match else
            ""
        )

        # ---------------------------------------------------
        # FALLBACKS
        # ---------------------------------------------------

        if len(title) < 15:

            title = (
                "महाभारत का ऐसा रहस्य जिसे बहुत कम लोग जानते हैं"
            )

        if len(description) < 20:

            description = (
                "भारत की रहस्यमयी कथाओं और पौराणिक रहस्यों के लिए "
                "RamLala10 को Subscribe करें।"
            )

        # Merge smart hashtags
        final_hashtags = []

        final_hashtags.extend(hashtags)
        final_hashtags.extend(keyword_tags)
        final_hashtags.extend(DEFAULT_HASHTAGS)

        # remove duplicates
        final_hashtags = list(
            dict.fromkeys(final_hashtags)
        )

        # keep only 10
        final_hashtags = final_hashtags[:10]

        return {

            "title": title,

            "description": (

                description
                + "\n\n"
                + " ".join(final_hashtags)
            ),

            "hashtags": " ".join(final_hashtags)
        }

    except Exception as e:

        print(f"\nMetadata Error: {e}")

        fallback_tags = (
            keyword_tags + DEFAULT_HASHTAGS
        )

        fallback_tags = list(
            dict.fromkeys(fallback_tags)
        )[:10]

        return {

            "title": (
                "महाभारत का ऐसा रहस्य जिसे बहुत कम लोग जानते हैं"
            ),

            "description": (
                "भारत की रहस्यमयी कथाओं और पौराणिक रहस्यों के लिए "
                "RamLala10 को Subscribe करें।\n\n"
                + " ".join(fallback_tags)
            ),

            "hashtags": " ".join(fallback_tags)
        }

# ---------------------------------------------------
# TEST
# ---------------------------------------------------

if __name__ == "__main__":

    sample_script = """
    हनुमानजी ने सूर्यदेव को फल समझकर निगल लिया था।
    उनकी शक्ति देखकर सभी देवता चौंक गए।
    """

    metadata = generate_metadata(
        sample_script
    )

    print("\nTITLE:\n")
    print(metadata["title"])

    print("\nDESCRIPTION:\n")
    print(metadata["description"])

    print("\nHASHTAGS:\n")
    print(metadata["hashtags"])