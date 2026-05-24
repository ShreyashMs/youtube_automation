from PIL import Image

# Pillow fix
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

from moviepy.editor import *
import os

def create_video():

    clips = []

    footage_folder = "assets/footage"

    video_files = [
        f"{footage_folder}/{file}"
        for file in os.listdir(footage_folder)
        if file.endswith(".mp4")
    ]

    for file in video_files:

        clip = VideoFileClip(file)

        clip = clip.resize(height=1920)

        if clip.w < 1080:
            clip = clip.resize(width=1080)

        clip = clip.crop(
            x_center=clip.w / 2,
            width=1080,
            height=1920
        )

        clip = clip.subclip(0, min(5, clip.duration))

        clips.append(clip)

    final_video = concatenate_videoclips(
        clips,
        method="compose"
    )

    # LOAD AUDIO
    audio = AudioFileClip("assets/audio/narration.wav")

    # MATCH VIDEO LENGTH TO AUDIO
    final_video = final_video.set_duration(audio.duration)

    # ADD AUDIO
    final_video = final_video.set_audio(audio)

    # EXPORT
    final_video.write_videofile(
        "output/final_short.mp4",
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        fps=30
    )

    print("Final video exported with sound!")