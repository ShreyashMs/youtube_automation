from PIL import Image

# ---------------------------------------------------
# PILLOW FIX
# ---------------------------------------------------

if not hasattr(Image, "ANTIALIAS"):

    Image.ANTIALIAS = Image.Resampling.LANCZOS

# ---------------------------------------------------
# IMPORTS
# ---------------------------------------------------

from moviepy.editor import *

from moviepy.video.tools.subtitles import (
    SubtitlesClip
)

from scripts.subtitle_generator import (
    generate_subtitles
)

import os
import random

# ---------------------------------------------------
# PATHS
# ---------------------------------------------------

FONT_PATH = (
    "assets/fonts/"
    "NotoSansDevanagari-Regular.ttf"
)

FOOTAGE_FOLDER = "assets/footage"

OUTPUT_PATH = (
    "output/final_short.mp4"
)

NARRATION_PATH = (
    "assets/audio/narration.wav"
)

# ---------------------------------------------------
# CHOOSE BGM
# ---------------------------------------------------

def choose_bgm(script_text):

    # sometimes no bgm
    if random.random() < 0.15:

        return None

    mappings = {

        "कृष्ण": [

            "assets/music/krishna.mp3",
            "assets/music/emotional.mp3",
        ],

        "शिव": [

            "assets/music/shiva.mp3",
            "assets/music/epic.mp3",
        ],

        "महाभारत": [

            "assets/music/epic.mp3",
            "assets/music/suspense.mp3",
        ],

        "रावण": [

            "assets/music/epic.mp3",
            "assets/music/dark.mp3",
        ],

        "हनुमान": [

            "assets/music/epic.mp3",
            "assets/music/emotional.mp3",
        ],

        "रहस्य": [

            "assets/music/suspense.mp3",
            "assets/music/suspense_2.mp3",
        ],

        "श्राप": [

            "assets/music/dark.mp3",
            "assets/music/suspense.mp3",
        ]
    }

    for keyword, tracks in mappings.items():

        if keyword in script_text:

            available = [

                track

                for track in tracks

                if os.path.exists(track)
            ]

            if available:

                return random.choice(
                    available
                )

    default_tracks = [

        "assets/music/emotional.mp3",
        "assets/music/suspense.mp3",
        "assets/music/epic.mp3",
    ]

    available = [

        track

        for track in default_tracks

        if os.path.exists(track)
    ]

    if available:

        return random.choice(
            available
        )

    return None

# ---------------------------------------------------
# PROCESS CLIP
# ---------------------------------------------------

def process_clip(

    file_path,

    target_duration
):

    clip = VideoFileClip(file_path)

    # ---------------------------------------------------
    # RANDOM SECTION
    # ---------------------------------------------------

    if clip.duration > target_duration:

        start = random.uniform(

            0,

            max(
                clip.duration
                - target_duration,
                0
            )
        )

        clip = clip.subclip(

            start,

            start + target_duration
        )

    else:

        clip = clip.loop(
            duration=target_duration
        )

    # ---------------------------------------------------
    # RESIZE
    # ---------------------------------------------------

    clip = clip.resize(height=1920)

    if clip.w < 1080:

        clip = clip.resize(width=1080)

    # ---------------------------------------------------
    # CROP
    # ---------------------------------------------------

    clip = clip.crop(

        x_center=clip.w / 2,

        width=1080,

        height=1920
    )

    # ---------------------------------------------------
    # EFFECTS
    # ---------------------------------------------------

    clip = (

        clip

        .fadein(0.25)

        .fadeout(0.25)
    )

    # subtle zoom
    zoom = random.uniform(
        1.02,
        1.08
    )

    clip = clip.resize(
        lambda t: zoom
    )

    return clip

# ---------------------------------------------------
# SUBTITLE GENERATOR
# ---------------------------------------------------

def subtitle_generator(txt):

    return TextClip(

        txt,

        fontsize=78,

        font=FONT_PATH,

        color="white",

        stroke_color="black",

        stroke_width=5,

        method="caption",

        align="center",

        size=(920, None)
    )

# ---------------------------------------------------
# CREATE VIDEO
# ---------------------------------------------------

def create_video():

    print("\nCreating final video...")

    # ---------------------------------------------------
    # LOAD FOOTAGE
    # ---------------------------------------------------

    if not os.path.exists(
        FOOTAGE_FOLDER
    ):

        raise Exception(
            "Footage folder missing"
        )

    video_files = [

        os.path.join(
            FOOTAGE_FOLDER,
            file
        )

        for file in os.listdir(
            FOOTAGE_FOLDER
        )

        if file.endswith(".mp4")
    ]

    if not video_files:

        raise Exception(
            "No footage found"
        )

    random.shuffle(video_files)

    # ---------------------------------------------------
    # LOAD NARRATION
    # ---------------------------------------------------

    if not os.path.exists(
        NARRATION_PATH
    ):

        raise Exception(
            "Narration file missing"
        )

    narration = AudioFileClip(
        NARRATION_PATH
    ).volumex(1.0)

    total_audio_duration = (
        narration.duration
    )

    print(
        f"Narration duration: "
        f"{round(total_audio_duration, 2)} sec"
    )

    # ---------------------------------------------------
    # PROCESS CLIPS
    # ---------------------------------------------------

    clips = []

    clip_duration = (

        total_audio_duration
        / len(video_files)
    )

    for file in video_files:

        try:

            print(
                f"Processing: {os.path.basename(file)}"
            )

            clip = process_clip(

                file,

                clip_duration
            )

            clips.append(clip)

        except Exception as e:

            print(
                f"\nError with {file}"
            )

            print(e)

    if not clips:

        raise Exception(
            "No usable clips found"
        )

    # ---------------------------------------------------
    # COMBINE VIDEO
    # ---------------------------------------------------

    final_video = concatenate_videoclips(

        clips,

        method="compose"
    )

    final_video = final_video.set_duration(
        narration.duration
    )

    # ---------------------------------------------------
    # LOAD SCRIPT
    # ---------------------------------------------------

    with open(

        "script.txt",

        "r",

        encoding="utf-8"

    ) as f:

        script_text = f.read()

    # ---------------------------------------------------
    # BACKGROUND MUSIC
    # ---------------------------------------------------

    bgm_path = choose_bgm(
        script_text
    )

    if bgm_path:

        print(
            f"\nUsing BGM:\n{bgm_path}"
        )

        bgm = AudioFileClip(
            bgm_path
        )

        bgm = bgm.volumex(0.05)

        bgm = afx.audio_loop(

            bgm,

            duration=narration.duration
        )

        final_audio = CompositeAudioClip([

            bgm,

            narration
        ])

    else:

        print("\nNo BGM selected")

        final_audio = narration

    final_video = final_video.set_audio(
        final_audio
    )

    # ---------------------------------------------------
    # GENERATE SUBTITLES
    # ---------------------------------------------------

    print("\nGenerating subtitles...")

    subtitle_segments = generate_subtitles(
        narration.duration
    )

    subtitles = []

    for segment in subtitle_segments:

        subtitles.append(

            (

                (
                    segment["start"],
                    segment["end"]
                ),

                segment["text"]
            )
        )

    print("\nSubtitle count:")
    print(len(subtitles))

    # ---------------------------------------------------
    # SUBTITLE CLIPS
    # ---------------------------------------------------

    subtitle_clips = SubtitlesClip(

        subtitles,

        subtitle_generator
    )

    subtitle_clips = subtitle_clips.set_position(

        ("center", 1450)
    )

    # ---------------------------------------------------
    # OVERLAY
    # ---------------------------------------------------

    final_video = CompositeVideoClip([

        final_video,

        subtitle_clips
    ])

    # ---------------------------------------------------
    # EXPORT
    # ---------------------------------------------------

    os.makedirs(
        "output",
        exist_ok=True
    )

    print("\nExporting video...")

    final_video.write_videofile(

        OUTPUT_PATH,

        codec="libx264",

        audio_codec="aac",

        temp_audiofile="temp-audio.m4a",

        remove_temp=True,

        fps=30,

        threads=4,

        preset="medium",

        bitrate="6000k"
    )

    print(
        "\nFinal video exported successfully!"
    )

    print(
        f"\nSaved to:\n{OUTPUT_PATH}"
    )

# ---------------------------------------------------
# TEST
# ---------------------------------------------------

if __name__ == "__main__":

    create_video()