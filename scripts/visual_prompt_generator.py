import re

VISUAL_MAP = {

    "शिव": [
        "cinematic shiva statue",
        "mahakal temple drone",
        "himalaya cinematic",
    ],

    "हनुमान": [
        "epic hanuman silhouette",
        "mountain sunrise cinematic",
        "flying clouds cinematic",
    ],

    "राम": [
        "ram mandir drone",
        "ancient india cinematic",
        "forest cinematic",
    ],

    "कृष्ण": [
        "krishna flute cinematic",
        "vrindavan temple",
        "peacock feather macro",
    ],

    "महाभारत": [
        "epic war cinematic",
        "battlefield drone",
        "ancient warriors",
    ],

    "रावण": [
        "dark king cinematic",
        "epic fire cinematic",
        "fantasy fort",
    ]
}

DEFAULT_VISUALS = [

    "ancient india cinematic",
    "hindu temple drone",
    "spiritual india",
    "epic clouds cinematic",
]

def generate_visual_prompts(script):

    prompts = []

    for keyword, visuals in VISUAL_MAP.items():

        if keyword in script:

            prompts.extend(visuals)

    if not prompts:

        prompts = DEFAULT_VISUALS

    prompts = list(set(prompts))

    return prompts

if __name__ == "__main__":

    sample = "हनुमानजी ने सूर्य को निगल लिया"

    result = generate_visual_prompts(sample)

    for r in result:
        print(r)