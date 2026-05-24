from scripts.script_generator import generate_script
from scripts.tts_generator import generate_voice
from scripts.fetch_footage import fetch_footage
from scripts.editor import create_video
from scripts.youtube_uploader import upload_video

import re

print("Generating script...")

response = generate_script()

# Save raw response
with open("raw_script.txt", "w", encoding="utf-8") as f:
    f.write(response)

# Remove markdown
response = response.replace("**", "")

# Extract sections
hook_match = re.search(
    r"HOOK:\s*(.*?)\s*SCRIPT:",
    response,
    re.DOTALL
)

script_match = re.search(
    r"SCRIPT:\s*(.*?)\s*CTA:",
    response,
    re.DOTALL
)

cta_match = re.search(
    r"CTA:\s*(.*)",
    response,
    re.DOTALL
)

hook = hook_match.group(1).strip() if hook_match else ""
script = script_match.group(1).strip() if script_match else ""
cta = cta_match.group(1).strip() if cta_match else ""

# Keep only first CTA line
cta = cta.split("\n")[0].strip()

final_script = f"{hook}\n\n{script}\n\n{cta}"

# Save narration script
with open("script.txt", "w", encoding="utf-8") as f:
    f.write(final_script)

print("\nFINAL SCRIPT:\n")
print(final_script)

# Fetch footage
print("\nFetching footage...")
fetch_footage("ancient temple")

# Generate voice
print("\nGenerating Hindi voice...")
generate_voice()

# Create video
print("\nCreating final short...")
create_video()

print("\nUploading to YouTube...")
upload_video()

print("\nPipeline completed successfully!")