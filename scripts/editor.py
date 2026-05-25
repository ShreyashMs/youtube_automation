from PIL import Image

# Pillow fix
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

from moviepy.editor import *

import os
import random


def create_video():

    footage_folder = "assets/footage"

    video_files = [
        f"{footage_folder}/{file}"
        for file in os.listdir(footage_folder)
        if file.endswith(".mp4")
    ]

    random.shuffle(video_files)

    narration = AudioFileClip(
        "assets/audio/narration.wav"
    )

    total_audio_duration = narration.duration

    clips = []

    # Duration per clip
    clip_duration = (
        total_audio_duration / max(len(video_files), 1)
    )

    for file in video_files:

        try:

            clip = VideoFileClip(file)

            # Random start point
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

            # Resize
            clip = clip.resize(height=1920)

            if clip.w < 1080:
                clip = clip.resize(width=1080)

            # Crop vertical
            clip = clip.crop(
                x_center=clip.w / 2,
                width=1080,
                height=1920
            )

            # Smooth fade
            clip = clip.fadein(0.3).fadeout(0.3)

            clips.append(clip)

        except Exception as e:

            print(f"Error processing {file}")
            print(e)

    final_video = concatenate_videoclips(
        clips,
        method="compose"
    )

    # Match narration
    final_video = final_video.set_duration(
        narration.duration
    )

    # Optional background music
    bgm_path = "assets/music/bgm.mp3"

    if os.path.exists(bgm_path):

        bgm = AudioFileClip(
            bgm_path
        ).volumex(0.08)

        bgm = bgm.loop(
            duration=narration.duration
        )

        final_audio = CompositeAudioClip([
            bgm,
            narration
        ])

    else:

        final_audio = narration

    final_video = final_video.set_audio(
        final_audio
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
        "Final video exported successfully!"
    )