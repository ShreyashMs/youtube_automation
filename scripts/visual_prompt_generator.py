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
    "lord brahma cosmic creation cinematic golden universe",
    "ancient pushkar temple cinematic sunrise aerial view",
    "king harishchandra royal court cinematic dramatic lighting",
    "cremation ground cinematic ancient india emotional atmosphere",
    "markandeya young sage praying before shivling cinematic storm",
    "yamraj appearing before devotee cinematic divine aura",
    "savitri confronting yamraj cinematic forest path",
    "nachiketa meeting yamraj cinematic mystical underworld gate",
    "dhruva child meditation under night sky cinematic stars",
    "prahlad surrounded by fire unharmed cinematic divine protection",
    "hiranyakashipu royal throne cinematic dark palace",
    "narasimha avatar emerging from pillar cinematic epic scene",
    "vamana avatar before king bali cinematic golden palace",
    "king bali donation ceremony cinematic divine atmosphere",
    "parashurama holding axe cinematic mountain landscape",
    "immortal warrior sage cinematic ancient india",
    "vishwamitra intense meditation cinematic forest ashram",
    "trishanku suspended between heaven and earth cinematic sky",
    "river ganga descending from heavens cinematic divine waterfall",
    "lord shiva catching ganga in matted hair cinematic",
    "sage agastya drinking ocean cinematic mythological epic",
    "ved vyasa writing ancient scripture cinematic candlelight",
    "lord ganesha writing mahabharata cinematic manuscript scene",
    "broken tusk ganesha cinematic closeup divine glow",
    "kartikeya riding peacock cinematic battlefield",
    "nandi guarding kailash temple cinematic snowfall",
    "kamadeva aiming flower arrow cinematic heavenly garden",
    "sati entering sacred fire cinematic emotional scene",
    "shakti peeth divine energy cinematic glowing temples",
    "maa kali defeating raktabija cinematic epic battle",
    "chamunda goddess fierce form cinematic dark sky",
    "navdurga divine forms cinematic celestial background",
    "kubera treasure palace cinematic golden wealth",
    "shukracharya meditating cinematic ancient cave",
    "brihaspati teaching devas cinematic heavenly court",
    "indra seated on celestial throne cinematic clouds",
    "airavata elephant emerging from cosmic ocean cinematic",
    "kamadhenu divine cow glowing aura cinematic",
    "syamantaka gem cinematic mystical golden light",
    "shani dev cosmic planet background cinematic",
    "rahu ketu celestial eclipse cinematic dark sky",
    "solar eclipse mythology cinematic cosmic scene",
    "chandra dev riding celestial chariot cinematic moonlight",
    "yaksha guardian spirit cinematic ancient forest",
    "gandharva celestial musicians cinematic heavenly realm",
    "apsara dancing in divine court cinematic golden light",
    "urvashi celestial beauty cinematic heavenly palace",
    "menaka descending from heaven cinematic forest",
    "tilottama divine creation cinematic celestial glow",
    "gajendra moksha elephant praying in lake cinematic",
    "sage jadabharata wandering silently cinematic spiritual landscape",
    "king janaka royal wisdom cinematic palace hall",
    "ashtavakra teaching kings cinematic philosophical atmosphere",
    "vidura advising royal court cinematic dramatic lighting",
    "kripacharya immortal warrior sage cinematic battlefield",
    "barbarik warrior with three arrows cinematic epic portrait",
    "barbarik severed head watching battlefield cinematic mystical scene",
    "ghatotkacha giant warrior cinematic night battle",
    "ulupi naga princess underwater kingdom cinematic",
    "chitrangada warrior princess cinematic royal battlefield",
    "arjuna exile journey cinematic forest landscape",
    "babruvahana defeating arjuna cinematic emotional battle",
    "king parikshit cursed by sage cinematic royal court",
    "takshaka naga king cinematic underground serpent kingdom",
    "sarpa yagna cinematic massive sacred fire ritual",
    "shukadeva narrating bhagavata cinematic riverbank scene",
    "kalki avatar riding white horse cinematic apocalypse sky",
    "future avatar cinematic divine warrior silhouette",
    "saptarishi constellation cinematic cosmic night sky",
    "seven immortal sages cinematic mountain meditation",
    "chiranjeevi immortals cinematic mystical gathering",
    "patal lok cinematic underground golden kingdom",
    "mount meru cinematic cosmic mountain center universe",
    "ancient hindu cosmology cinematic galaxy visualization",
    "time cycle of yugas cinematic cosmic clock",
    "soul journey after death cinematic spiritual pathway",
    "garuda purana underworld journey cinematic mystical realm",
    "celestial gates of heaven cinematic golden clouds",
    "divine cosmic balance cinematic universe energy",
    "ancient india mythological kingdom cinematic aerial view",
    "epic hindu mythology cinematic universe background",
    "divine aura glowing temple cinematic night",
    "spiritual india golden light meditation landscape",
    "temple bells cinematic slow motion fog",
    "ancient stone carvings cinematic macro details",
    "himalayan cave cinematic yogi meditation",
    "holy pilgrimage cinematic mountain path",
    "river ganga cinematic sunrise holy water reflections",
    "vedic fire ritual cinematic close up flames",
    "cosmic divine light cinematic sacred atmosphere"
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