from scripts.script_generator import generate_script
from scripts.metadata_generator import generate_metadata
from scripts.tts_generator import generate_voice
from scripts.fetch_footage import fetch_footage
from scripts.editor import create_video
from scripts.youtube_uploader import upload_video

import os
import random

# ---------------------------------------------------
# FOOTAGE QUERIES
# ---------------------------------------------------

FOOTAGE_QUERIES = {

    "राम": [
        "ram temple",
        "lord rama statue",
        "ramayan cinematic",
        "ancient india temple",
        "ram ji art"
    ],

    "हनुमान": [
        "hanuman statue",
        "hanuman cinematic",
        "hanuman temple",
        "epic monkey warrior",
        "hanuman art"
    ],

    "शिव": [
        "shiva statue",
        "mahakal temple",
        "shivling",
        "shiva cinematic",
        "kedarnath temple"
    ],

    "कृष्ण": [
        "krishna temple",
        "krishna flute",
        "vrindavan temple",
        "krishna cinematic",
        "bhagavad gita art"
    ],

    "विष्णु": [
        "vishnu statue",
        "lord vishnu art",
        "ancient temple india",
        "vishnu cinematic"
    ],

    "दुर्गा": [
        "durga maa",
        "navratri cinematic",
        "durga temple",
        "maa durga statue"
    ],

    "गणेश": [
        "ganesh statue",
        "ganpati temple",
        "ganesh cinematic",
        "ganpati bappa"
    ],

    "रावण": [
        "ravan art",
        "ramayan war",
        "epic war cinematic",
        "lanka cinematic"
    ],

    "महाभारत": [
        "mahabharat art",
        "kurukshetra war",
        "epic indian war",
        "bhishma art"
    ],

    "DEFAULT": [
        "ancient india",
        "hindu temple",
        "cinematic temple",
        "mystic india",
        "ancient ruins"
    ]
}

# ---------------------------------------------------
# DETECT FOOTAGE QUERY
# ---------------------------------------------------

def get_footage_query(script):

    for keyword, queries in FOOTAGE_QUERIES.items():

        if keyword in script:

            return random.choice(queries)

    return random.choice(
        FOOTAGE_QUERIES["DEFAULT"]
    )

# ---------------------------------------------------
# GENERATE SCRIPT
# ---------------------------------------------------

print("\nGenerating script...\n")

script = generate_script()

# Safety check
if not script or len(script.strip()) == 0:

    raise ValueError(
        "Generated script is empty"
    )

# ---------------------------------------------------
# SAVE SCRIPT
# ---------------------------------------------------

with open(
    "script.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(script.strip())

print("\nFINAL SCRIPT:\n")
print(script)

# ---------------------------------------------------
# GENERATE METADATA
# ---------------------------------------------------

print("\nGenerating metadata...\n")

try:

    metadata = generate_metadata(script)

    title = metadata.get(
        "title",
        "पौराणिक रहस्य"
    )

    description = metadata.get(
        "description",
        "ऐसी और कहानियों के लिए रामलला१० को फॉलो करें।"
    )

    hashtags = metadata.get(
        "hashtags",
        "#राम #महाभारत #पौराणिककथा"
    )

except Exception as e:

    print("\nMetadata generation failed")
    print(e)

    title = "पौराणिक रहस्य"

    description = (
        "ऐसी और कहानियों के लिए "
        "रामलला१० को फॉलो करें।"
    )

    hashtags = (
        "#राम #महाभारत #पौराणिककथा"
    )

# ---------------------------------------------------
# CLEAN METADATA
# ---------------------------------------------------

title = (
    title
    .replace("**", "")
    .replace('"', "")
    .strip()
)

description = (
    description
    .replace("**", "")
    .replace('"', "")
    .strip()
)

hashtags = (
    hashtags
    .replace("**", "")
    .replace('"', "")
    .strip()
)

full_description = (
    f"{description}\n\n{hashtags}"
)

# ---------------------------------------------------
# SAVE METADATA
# ---------------------------------------------------

with open(
    "video_metadata.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(f"TITLE:\n{title}\n\n")

    f.write(
        f"DESCRIPTION:\n{full_description}"
    )

print("\nTITLE:\n")
print(title)

print("\nDESCRIPTION:\n")
print(full_description)

# ---------------------------------------------------
# FETCH FOOTAGE
# ---------------------------------------------------

query = get_footage_query(script)

print("\nFetching footage...")
print(f"Using query: {query}")

fetch_footage(query)

# ---------------------------------------------------
# VERIFY SCRIPT FILE
# ---------------------------------------------------

if not os.path.exists("script.txt"):

    raise FileNotFoundError(
        "script.txt not found"
    )

with open(
    "script.txt",
    "r",
    encoding="utf-8"
) as f:

    saved_script = f.read().strip()

if len(saved_script) == 0:

    raise ValueError(
        "script.txt is empty"
    )

print("\nSCRIPT FILE VERIFIED\n")

# ---------------------------------------------------
# GENERATE VOICE
# ---------------------------------------------------

print("\nGenerating Hindi voice...")

generate_voice()

print("\nVoice generated successfully!")

# ---------------------------------------------------
# CREATE VIDEO
# ---------------------------------------------------

print("\nCreating final short...")

create_video()

# ---------------------------------------------------
# VERIFY VIDEO
# ---------------------------------------------------

if not os.path.exists(
    "output/final_short.mp4"
):

    raise FileNotFoundError(
        "Final video not created"
    )

print(
    "\nFinal video exported successfully!"
)

# ---------------------------------------------------
# UPLOAD TO YOUTUBE
# ---------------------------------------------------

print("\nUploading to YouTube...")

try:

    upload_video(
        title=title,
        description=full_description
    )

    print(
        "\nVideo uploaded successfully!"
    )

except Exception as e:

    print("\nUpload failed:")
    print(e)

print(
    "\nPipeline completed successfully!"
)