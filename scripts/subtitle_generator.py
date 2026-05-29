import whisper
import re

# ---------------------------------------------------
# CLEAN HINDI TEXT
# ---------------------------------------------------

def clean_text(text):

    text = text.strip()

    # remove weird symbols
    text = re.sub(r'\s+', ' ', text)

    return text


# ---------------------------------------------------
# GENERATE SUBTITLES
# ---------------------------------------------------

def generate_subtitles():

    model = whisper.load_model("base")

    result = model.transcribe(
        "assets/audio/narration.wav",
        language="hi",
        task="transcribe"
    )

    subtitles = []

    for segment in result["segments"]:

        subtitles.append({

            "start": segment["start"],

            "end": segment["end"],

            "text": clean_text(segment["text"])
        })

    return subtitles