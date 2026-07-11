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

try:
    from .subtitle_generator import (
        generate_subtitles
    )
except ImportError:
    from subtitle_generator import (
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

def choose_bgm(script_text, emotion=None):

    emotion_tracks = {
        "peaceful": ["assets/music/krishna.mp3", "assets/music/emotional.mp3"],
        "emotional": ["assets/music/emotional.mp3"],
        "mysterious": ["assets/music/suspense.mp3", "assets/music/suspense_2.mp3"],
        "intense": ["assets/music/epic.mp3", "assets/music/suspense.mp3"],
        "devotional": ["assets/music/krishna.mp3", "assets/music/shiva.mp3"],
    }
    if emotion in emotion_tracks:
        available = [track for track in emotion_tracks[emotion] if os.path.exists(track)]
        if available:
            return random.choice(available)

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

def subtitle_generator(txt, style=None):
    style = style or {}

    return TextClip(

        txt,

        fontsize=style.get("font_size", 78),

        font=FONT_PATH,

        color=style.get("color", "white"),

        stroke_color=style.get("stroke_color", "black"),

        stroke_width=style.get("stroke_width", 5),

        method="caption",

        align="center",

        size=(920, None)
    )

# ---------------------------------------------------
# CREATE VIDEO
# ---------------------------------------------------

def create_video(render_settings=None):

    print("\nCreating final video...")
    render_settings = render_settings or {}

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

    music_settings = render_settings.get("music", {})
    if music_settings is None:
        music_settings = {"enabled": False}
    if music_settings.get("enabled") is False:
        bgm_path = None
    else:
        bgm_path = music_settings.get("file") or choose_bgm(
            script_text,
            render_settings.get("emotion"),
        )
    if bgm_path and not os.path.exists(bgm_path):
        raise FileNotFoundError(f"Configured music file not found: {bgm_path}")

    if bgm_path:

        print(
            f"\nUsing BGM:\n{bgm_path}"
        )

        bgm = AudioFileClip(
            bgm_path
        )

        bgm = bgm.volumex(float(music_settings.get("volume", 0.05)))

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

    subtitle_settings = render_settings.get("subtitles", {"enabled": True})
    if subtitle_settings is None:
        subtitle_settings = {"enabled": False}
    if subtitle_settings.get("enabled") is False:
        subtitle_settings = {"enabled": False}
    else:
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

            lambda text: subtitle_generator(text, subtitle_settings)
        )

        subtitle_clips = subtitle_clips.set_position(

            ("center", subtitle_settings.get("position_y", 1450))
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
