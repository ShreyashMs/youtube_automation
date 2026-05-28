import whisper
import ssl

# ----------------------------------------
# FIX SSL ISSUE (macOS Python)
# ----------------------------------------

ssl._create_default_https_context = (
    ssl._create_unverified_context
)

# ----------------------------------------
# LOAD WHISPER MODEL ONCE
# ----------------------------------------

model = whisper.load_model("base")

# ----------------------------------------
# GENERATE SUBTITLES
# ----------------------------------------

def generate_subtitles():

    result = model.transcribe(
        "assets/audio/narration.wav",
        language="hi",
        fp16=False
    )

    return result["segments"]


# ----------------------------------------
# TEST
# ----------------------------------------

if __name__ == "__main__":

    subtitles = generate_subtitles()

    for segment in subtitles:

        print(
            f"[{segment['start']:.2f} - "
            f"{segment['end']:.2f}] "
            f"{segment['text']}"
        )