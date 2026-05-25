from scripts.script_generator import generate_script
from scripts.metadata_generator import generate_metadata
from scripts.tts_generator import generate_voice
from scripts.fetch_footage import fetch_footage
from scripts.editor import create_video
from scripts.youtube_uploader import upload_video

import re
import random

# RANDOM FOOTAGE SEARCHES
FOOTAGE_QUERIES = [
    "ancient india",
    "hindu temple",
    "mahabharat art",
    "epic war",
    "cinematic temple",
    "indian history",
    "shiva statue",
    "ramayan temple",
    "ancient ruins",
    "mystic india"
]

print("Generating script...")

response = generate_script()

# SAVE RAW RESPONSE
with open("raw_script.txt", "w", encoding="utf-8") as f:
    f.write(response)

# CLEAN MARKDOWN
response = response.replace("**", "")

# EXTRACT HOOK
hook_match = re.search(
    r"HOOK:\s*(.*?)\s*SCRIPT:",
    response,
    re.DOTALL
)

# EXTRACT SCRIPT
script_match = re.search(
    r"SCRIPT:\s*(.*?)\s*CTA:",
    response,
    re.DOTALL
)

# EXTRACT CTA
cta_match = re.search(
    r"CTA:\s*(.*)",
    response,
    re.DOTALL
)

hook = hook_match.group(1).strip() if hook_match else ""

script = (
    script_match.group(1).strip()
    if script_match else ""
)

cta = (
    cta_match.group(1).strip()
    if cta_match else ""
)

# KEEP ONLY FIRST CTA LINE
cta = cta.split("\n")[0].strip()

# FINAL NARRATION
final_script = f"{hook}\n\n{script}\n\n{cta}"

# SAVE SCRIPT
with open("script.txt", "w", encoding="utf-8") as f:
    f.write(final_script)

print("\nFINAL SCRIPT:\n")
print(final_script)

# GENERATE TITLE + DESCRIPTION + TAGS
print("\nGenerating metadata...")

metadata = generate_metadata(final_script)

title = metadata["title"]
description = metadata["description"]
hashtags = metadata["hashtags"]

# FINAL DESCRIPTION
full_description = (
    f"{description}\n\n{hashtags}"
)

# SAVE METADATA
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

# RANDOM FOOTAGE SEARCH
query = random.choice(FOOTAGE_QUERIES)

print("\nFetching footage...")
print(f"Using query: {query}")

fetch_footage(query)

# GENERATE VOICE
print("\nGenerating Hindi voice...")
generate_voice()

# CREATE VIDEO
print("\nCreating final short...")
create_video()

# UPLOAD TO YOUTUBE
print("\nUploading to YouTube...")

upload_video(
    title=title,
    description=full_description
)

print("\nPipeline completed successfully!")