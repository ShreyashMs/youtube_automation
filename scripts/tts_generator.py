import subprocess
import os
import wave
import contextlib
import re

# ---------------------------------------------------
# PATHS
# ---------------------------------------------------

PIPER_PATH = (
    "/Users/shreyashmahalle/"
    "Youtube_Automation/venv/bin/piper"
)

MODEL_PATH = (
    "assets/models/"
    "hi_IN-rohan-medium.onnx"
)

OUTPUT_DIR = "assets/audio"

OUTPUT_PATH = (
    f"{OUTPUT_DIR}/narration.wav"
)

# ---------------------------------------------------
# CLEAN SCRIPT
# ---------------------------------------------------

def clean_script(text):

    text = text.strip()

    # remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # better pauses
    text = text.replace("।", "। ")
    text = text.replace("!", "! ")
    text = text.replace("?", "? ")

    return text.strip()

# ---------------------------------------------------
# AUDIO DURATION
# ---------------------------------------------------

def get_audio_duration(audio_path):

    with contextlib.closing(

        wave.open(audio_path, "r")

    ) as wf:

        frames = wf.getnframes()

        rate = wf.getframerate()

        duration = frames / float(rate)

        return round(duration, 2)

# ---------------------------------------------------
# GENERATE VOICE
# ---------------------------------------------------

def generate_voice():

    print("\nGenerating narration...")

    # ---------------------------------------------------
    # CHECK MODEL
    # ---------------------------------------------------

    if not os.path.exists(MODEL_PATH):

        raise FileNotFoundError(

            f"Piper model not found:\n{MODEL_PATH}"
        )

    # ---------------------------------------------------
    # CHECK PIPER
    # ---------------------------------------------------

    if not os.path.exists(PIPER_PATH):

        raise FileNotFoundError(

            f"Piper executable not found:\n{PIPER_PATH}"
        )

    # ---------------------------------------------------
    # CREATE OUTPUT DIR
    # ---------------------------------------------------

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    # ---------------------------------------------------
    # DELETE OLD AUDIO
    # ---------------------------------------------------

    if os.path.exists(OUTPUT_PATH):

        os.remove(OUTPUT_PATH)

    # ---------------------------------------------------
    # LOAD SCRIPT
    # ---------------------------------------------------

    with open(

        "script.txt",

        "r",

        encoding="utf-8"

    ) as f:

        text = f.read().strip()

    # ---------------------------------------------------
    # VALIDATE SCRIPT
    # ---------------------------------------------------

    if not text:

        raise ValueError(
            "script.txt is empty"
        )

    if len(text) < 30:

        raise ValueError(
            "Script too short"
        )

    text = clean_script(text)

    # ---------------------------------------------------
    # GENERATE AUDIO
    # ---------------------------------------------------

    process = subprocess.Popen(

        [

            PIPER_PATH,

            "--model",
            MODEL_PATH,

            "--output_file",
            OUTPUT_PATH
        ],

        stdin=subprocess.PIPE,

        stdout=subprocess.PIPE,

        stderr=subprocess.PIPE,

        text=True
    )

    stdout, stderr = process.communicate(text)

    # ---------------------------------------------------
    # CHECK SUCCESS
    # ---------------------------------------------------

    if process.returncode != 0:

        print("\nPIPER ERROR:\n")
        print(stderr)

        raise Exception(
            "Voice generation failed"
        )

    # ---------------------------------------------------
    # CHECK OUTPUT FILE
    # ---------------------------------------------------

    if not os.path.exists(OUTPUT_PATH):

        raise Exception(
            "Narration file not created"
        )

    # ---------------------------------------------------
    # CHECK FILE SIZE
    # ---------------------------------------------------

    file_size = os.path.getsize(
        OUTPUT_PATH
    )

    if file_size < 1000:

        raise Exception(
            "Generated audio is corrupted"
        )

    # ---------------------------------------------------
    # GET DURATION
    # ---------------------------------------------------

    duration = get_audio_duration(
        OUTPUT_PATH
    )

    print("\nVoice generated successfully!")

    print(
        f"Audio duration: {duration} seconds"
    )

    print(
        f"Saved to: {OUTPUT_PATH}"
    )

    return {

        "audio_path": OUTPUT_PATH,

        "duration": duration
    }

# ---------------------------------------------------
# TEST
# ---------------------------------------------------

if __name__ == "__main__":

    result = generate_voice()

    print("\nRESULT:\n")
    print(result)