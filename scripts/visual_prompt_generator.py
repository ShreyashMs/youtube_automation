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
    ],
    "कर्ण": [
    "epic warrior cinematic",
    "sunrise warrior",
    "ancient battlefield",
    "royal warrior armor",
    ],

    "अर्जुन": [
        "archer cinematic",
        "warrior with bow",
        "battlefield cinematic",
        "epic arrow slow motion",
    ],

    "भीष्म": [
        "old warrior cinematic",
        "epic battlefield",
        "ancient india war",
        "warrior meditation",
    ],

    "द्रौपदी": [
        "queen cinematic",
        "ancient palace india",
        "royal woman silhouette",
        "epic palace cinematic",
    ],

    "अभिमन्यु": [
        "young warrior cinematic",
        "battlefield smoke",
        "epic warrior",
        "war cinematic",
    ],

    "परशुराम": [
        "axe warrior cinematic",
        "forest warrior",
        "epic sage cinematic",
        "ancient warrior",
    ],

    "रावण": [
        "dark king cinematic",
        "fire cinematic",
        "epic villain",
        "dark temple cinematic",
    ],
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