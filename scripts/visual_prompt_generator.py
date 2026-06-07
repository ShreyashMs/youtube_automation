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

    "ancient india cinematic ruins",
    "hindu temple drone aerial view sunrise",
    "spiritual india golden light meditation landscape",
    "epic clouds cinematic storm over mountains",
    "ancient indian kingdom cinematic battle scene",
    "vedic era cinematic forest ashram",
    "temple bells cinematic slow motion fog",
    "river ganga cinematic sunrise holy water reflections",
    "himachal temples aerial drone cinematic",
    "ancient fort india cinematic dusk lighting",
    "mystic forest india cinematic fog rays",
    "divine aura glowing temple cinematic night",
    "hindu mythology cinematic battlefield sky fire",
    "ancient indian city cinematic golden hour",
    "desert temple ruins cinematic wind sand",
    "spiritual monk meditation cinematic mountains",
    "shiv temple himalayas cinematic snow clouds",
    "epic sky cinematic lightning over ancient land",
    "ancient india trading city cinematic port",
    "golden temple reflection cinematic water night",
    "vedic fire ritual cinematic close up flames",
    "ancient warriors cinematic slow motion armor",
    "temple corridor cinematic ultra detailed carvings",
    "spiritual energy cinematic glowing particles",
    "ancient india palace cinematic royal architecture",
    "moonlight temple cinematic mystic ambience",
    "riverbank rituals cinematic india evening",
    "ancient cave temple cinematic torchlight shadows",
    "holy pilgrimage cinematic mountain path",
    "divine hindu god aura cinematic glow silhouette",
    "epic battlefield cinematic dust clouds horses",
    "ancient scripts vedic manuscripts cinematic close up",
    "temple tower gopuram cinematic sunrise haze",
    "forest hermitage cinematic peaceful aura",
    "ancient india kingdom aerial cinematic vast landscape",
    "spiritual river crossing cinematic boats mist",
    "mythological scene cinematic divine weapons light",
    "ancient stone carvings cinematic macro details",
    "temple reflection water cinematic symmetry",
    "cosmic hindu mythology cinematic universe background",
    "ancient india festival cinematic lights crowd",
    "desert ruins cinematic sunset dramatic shadows",
    "holy ash ritual cinematic sacred fire",
    "ancient sages cinematic meditation aura glow",
    "himalayan cave cinematic yogi meditation",
    "temple bells ringing cinematic slow motion dust",
    "epic divine war cinematic clouds split sky",
    "ancient india marketplace cinematic bustling crowd",
    "spiritual awakening cinematic light burst human silhouette",
    "mythical river gods cinematic fantasy style"
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