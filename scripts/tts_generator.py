import subprocess
import os

PIPER_PATH = "/Users/shreyashmahalle/Youtube_Automation/venv/bin/piper"

MODEL_PATH = "assets/models/hi_IN-rohan-medium.onnx"

OUTPUT_PATH = "assets/audio/narration.wav"


def generate_voice():

    # Check model exists
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Piper model not found: {MODEL_PATH}"
        )

    # Read script
    with open("script.txt", "r", encoding="utf-8") as f:
        text = f.read().strip()

    # Check script is not empty
    if not text:
        raise ValueError("script.txt is empty")

    # Run Piper
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

    # Check success
    if process.returncode != 0:
        print(stderr)
        raise Exception("Voice generation failed")

    # Check output file
    if not os.path.exists(OUTPUT_PATH):
        raise Exception("Narration file not created")

    print("Voice generated successfully!")