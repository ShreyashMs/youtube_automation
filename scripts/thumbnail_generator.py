from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import os

WIDTH = 1280
HEIGHT = 720

FONT_PATH = (
    "assets/fonts/"
    "NotoSansDevanagari-Regular.ttf"
)

OUTPUT_PATH = (
    "output/thumbnail.jpg"
)

def create_thumbnail(title):

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        color=(10, 10, 10)
    )

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(
        FONT_PATH,
        70
    )

    wrapped = "\n".join(

        title[i:i+15]

        for i in range(
            0,
            len(title),
            15
        )
    )

    bbox = draw.textbbox(

        (0, 0),

        wrapped,

        font=font
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (WIDTH - text_width) / 2
    y = (HEIGHT - text_height) / 2

    draw.text(

        (x, y),

        wrapped,

        font=font,

        fill="white",

        stroke_width=4,

        stroke_fill="black"
    )

    os.makedirs(
        "output",
        exist_ok=True
    )

    image.save(
        OUTPUT_PATH,
        quality=95
    )

    print(
        f"Thumbnail saved:\n{OUTPUT_PATH}"
    )

if __name__ == "__main__":

    create_thumbnail(
        "हनुमानजी ने सूर्य को क्यों निगला"
    )