import re

# ---------------------------------------------------
# CLEAN TEXT
# ---------------------------------------------------

def clean_text(text):

    text = text.replace("\n", " ")

    text = re.sub(
        r'\s+',
        ' ',
        text
    )

    return text.strip()


# ---------------------------------------------------
# GENERATE SUBTITLES FROM SCRIPT
# ---------------------------------------------------

def generate_subtitles(duration):

    with open(
        "script.txt",
        "r",
        encoding="utf-8"
    ) as f:

        script = f.read()

    script = clean_text(script)

    # Split sentences
    sentences = re.split(
        r'(?<=[।!?])',
        script
    )

    sentences = [
        s.strip()
        for s in sentences
        if s.strip()
    ]

    subtitles = []

    subtitle_duration = (
        duration / max(len(sentences), 1)
    )

    current_time = 0

    for sentence in sentences:

        subtitles.append({

            "start": current_time,

            "end": current_time + subtitle_duration,

            "text": sentence
        })

        current_time += subtitle_duration

    return subtitles