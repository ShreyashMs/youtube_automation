import random

# ---------------------------------------------------

# VISUAL STYLES

# ---------------------------------------------------

VISUAL_STYLES = {


"शिव": [

    "mahakal temple cinematic",
    "shiva statue closeup",
    "himalaya cinematic",
    "meditation mountain",
    "shivling dramatic lighting",
    "ancient temple india",
    "cinematic fire smoke",
],

"राम": [

    "ram mandir cinematic",
    "ancient india aerial",
    "forest cinematic",
    "epic warrior silhouette",
    "indian temple sunset",
    "ramayan atmosphere",
],

"हनुमान": [

    "hanuman statue cinematic",
    "sunrise sky dramatic",
    "epic mountain cinematic",
    "flying warrior silhouette",
    "indian mythology cinematic",
    "storm clouds dramatic",
],

"कृष्ण": [

    "krishna flute cinematic",
    "vrindavan temple",
    "peacock feather macro",
    "river sunset india",
    "spiritual cinematic lighting",
    "bhagavad gita aesthetic",
],

"महाभारत": [

    "epic battlefield cinematic",
    "ancient warriors",
    "fire sparks slow motion",
    "kurukshetra atmosphere",
    "dark clouds battlefield",
    "cinematic war scene",
]


}

# ---------------------------------------------------

# DEFAULT VISUALS

# ---------------------------------------------------

DEFAULT_VISUALS = [


"ancient india cinematic",
"hindu temple drone",
"epic sky cinematic",
"indian spirituality",
"mystic cinematic visuals",


]

# ---------------------------------------------------

# GENERATE VISUAL PROMPTS

# ---------------------------------------------------

def generate_visual_prompts(script):


prompts = []

for keyword, visuals in VISUAL_STYLES.items():

    if keyword in script:

        prompts.extend(visuals)

if not prompts:

    prompts = DEFAULT_VISUALS

random.shuffle(prompts)

return prompts[:6]


# ---------------------------------------------------

# MAIN

# ---------------------------------------------------

if **name** == "**main**":


test_script = "हनुमानजी ने सूर्य को निगल लिया"

print(
    generate_visual_prompts(
        test_script
    )
)

