from PIL import Image

# ---------------------------------------------------
# PILLOW FIX
# ---------------------------------------------------

if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

from scripts.subtitle_generator import generate_subtitles

import os
import random

# ---------------------------------------------------
# FONT
# ---------------------------------------------------

FONT_PATH = "assets/fonts/NotoSansDevanagari-Regular.ttf"

# ---------------------------------------------------
# CHOOSE BGM
# ---------------------------------------------------

def choose_bgm(script_text):

    # Randomly disable BGM sometimes
    if random.random() < 0.20:
        return None

    if "कृष्ण" in script_text:

        return random.choice([
            "assets/music/krishna.mp3",
            "assets/music/emotional.mp3"
        ])

    if "शिव" in script_text:

        return random.choice([
            "assets/music/shiva.mp3",
            "assets/music/epic.mp3"
        ])

    if (
        "युद्ध" in script_text
        or "महाभारत" in script_text
        or "रावण" in script_text
    ):

        return random.choice([
            "assets/music/epic.mp3",
            "assets/music/suspense.mp3"
        ])

    if (
        "श्राप" in script_text
        or "रहस्य" in script_text
        or "भविष्यवाणी" in script_text
    ):

        return random.choice([
            "assets/music/suspense.mp3",
            "assets/music/suspense_2.mp3"
        ])

    return random.choice([
        "assets/music/emotional.mp3",
        "assets/music/suspense.mp3",
        "assets/music/epic.mp3"
    ])


# ---------------------------------------------------
# CREATE VIDEO
# ---------------------------------------------------

def create_video():

    footage_folder = "assets/footage"

    video_files = [

        f"{footage_folder}/{file}"

        for file in os.listdir(footage_folder)

        if file.endswith(".mp4")
    ]

    if not video_files:
        raise Exception("No footage found")

    random.shuffle(video_files)

    # ---------------------------------------------------
    # LOAD NARRATION
    # ---------------------------------------------------

    narration = AudioFileClip(
        "assets/audio/narration.wav"
    ).volumex(1.0)

    total_audio_duration = narration.duration

    clips = []

    clip_duration = (
        total_audio_duration / len(video_files)
    )

    # ---------------------------------------------------
    # PROCESS VIDEO CLIPS
    # ---------------------------------------------------

    for file in video_files:

        try:

            clip = VideoFileClip(file)

            # Random clip section
            if clip.duration > clip_duration:

                start = random.uniform(
                    0,
                    clip.duration - clip_duration
                )

                clip = clip.subclip(
                    start,
                    start + clip_duration
                )

            else:

                clip = clip.loop(
                    duration=clip_duration
                )

            # Resize for vertical shorts
            clip = clip.resize(height=1920)

            if clip.w < 1080:

                clip = clip.resize(width=1080)

            # Crop vertical
            clip = clip.crop(
                x_center=clip.w / 2,
                width=1080,
                height=1920
            )

            # Smooth fades
            clip = (
                clip
                .fadein(0.3)
                .fadeout(0.3)
            )

            clips.append(clip)

        except Exception as e:

            print(f"\nError processing: {file}")
            print(e)

    # ---------------------------------------------------
    # COMBINE CLIPS
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
    # SELECT BGM
    # ---------------------------------------------------

    bgm_path = choose_bgm(script_text)

    if (
        bgm_path
        and os.path.exists(bgm_path)
    ):

        print(f"\nUsing BGM: {bgm_path}")

        bgm = AudioFileClip(
            bgm_path
        ).volumex(0.03)

        bgm = bgm.audio_loop(
            duration=narration.duration
        )

        final_audio = CompositeAudioClip([
            bgm,
            narration
        ])

    else:

        print("\nNo BGM selected")

        final_audio = narration

    # Set final audio
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

        start = segment["start"]
        end = segment["end"]
        text = segment["text"]

        subtitles.append(
            (
                (start, end),
                text
            )
        )

    print("\nSample subtitles:")
    print(subtitles[:3])

    # ---------------------------------------------------
    # SUBTITLE STYLE
    # ---------------------------------------------------

    # ---------------------------------------------------
    # SUBTITLE STYLE
    # ---------------------------------------------------

    generator = lambda txt: TextClip(

        txt,

        fontsize=80,

        font=FONT_PATH,

        color="white",

        stroke_color="black",

        stroke_width=5,

        method="caption",

        align="center",

        size=(950, None)
    )

    # ---------------------------------------------------
    # CREATE SUBTITLE CLIPS
    # ---------------------------------------------------

    subtitle_clips = SubtitlesClip(
    subtitles,
    generator
    )

    subtitle_clips = subtitle_clips.set_position(
    ("center", 1400)
    )

    # ---------------------------------------------------
    # OVERLAY SUBTITLES
    # ---------------------------------------------------

    final_video = CompositeVideoClip([
        final_video,
        subtitle_clips
    ])

    # ---------------------------------------------------
    # EXPORT VIDEO
    # ---------------------------------------------------

    os.makedirs(
        "output",
        exist_ok=True
    )

    final_video.write_videofile(

        "output/final_short.mp4",

        codec="libx264",

        audio_codec="aac",

        temp_audiofile="temp-audio.m4a",

        remove_temp=True,

        fps=30,

        threads=4,

        preset="medium"
    )

    print(
        "\nFinal video exported successfully!"
    )