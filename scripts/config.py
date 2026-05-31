import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------
# API KEYS
# ---------------------------------------------------

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# ---------------------------------------------------
# PATHS
# ---------------------------------------------------

SCRIPT_PATH = "script.txt"

OUTPUT_VIDEO = "output/final_short.mp4"

NARRATION_AUDIO = "assets/audio/narration.wav"

FOOTAGE_DIR = "assets/footage"

FONT_PATH = "assets/fonts/NotoSansDevanagari-Regular.ttf"

# ---------------------------------------------------
# PIPER
# ---------------------------------------------------

PIPER_PATH = os.getenv(
    "PIPER_PATH",
    "/Users/shreyashmahalle/Youtube_Automation/venv/bin/piper"
)

PIPER_MODEL = os.getenv(
    "PIPER_MODEL",
    "assets/models/hi_IN-rohan-medium.onnx"
)

# ---------------------------------------------------
# VIDEO SETTINGS
# ---------------------------------------------------

VIDEO_WIDTH = 1080

VIDEO_HEIGHT = 1920

FPS = 30

MIN_FOOTAGE_CLIPS = 5

MAX_FOOTAGE_CLIPS = 8

# ---------------------------------------------------
# YOUTUBE
# ---------------------------------------------------

YOUTUBE_CATEGORY = "22"

DEFAULT_TAGS = [

    "रामायण",
    "महाभारत",
    "हिंदू",
    "mythology",
    "hinduism",
    "bharat",
    "shorts"
]