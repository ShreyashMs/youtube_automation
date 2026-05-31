from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter

import random
import os

# ---------------------------------------------------

# PATHS

# ---------------------------------------------------

FONT_PATH = (
"assets/fonts/"
"NotoSansDevanagari-Regular.ttf"
)

OUTPUT_PATH = (
"output/thumbnails"
)

# ---------------------------------------------------

# COLORS

# ---------------------------------------------------

TEXT_COLORS = [


"white",
"yellow",
"orange",
"gold"


]

# ---------------------------------------------------

# CLEAN TITLE

# ---------------------------------------------------

def clean_title(title):


title = title.replace(
    "**",
    ""
)

title = title.replace(
    '"',
    ""
)

return title.strip()


# ---------------------------------------------------

# CREATE BACKGROUND

# ---------------------------------------------------

def create_background():


width = 1280
height = 720

image = Image.new(
    "RGB",
    (width, height),
    (
        random.randint(10, 40),
        random.randint(10, 40),
        random.randint(10, 40)
    )
)

image = image.filter(
    ImageFilter.GaussianBlur(1)
)

return image


# ---------------------------------------------------

# DRAW TEXT

# ---------------------------------------------------

def draw_title(


image,
title


):


draw = ImageDraw.Draw(image)

font = ImageFont.truetype(
    FONT_PATH,
    70
)

title = clean_title(title)

text_color = random.choice(
    TEXT_COLORS
)

stroke_color = "black"

max_width = 1000

words = title.split()

lines = []
current_line = ""

# ---------------------------------------------------
# WRAP TEXT
# ---------------------------------------------------

for word in words:

    test_line = (
        current_line + " " + word
    ).strip()

    bbox = draw.textbbox(
        (0, 0),
        test_line,
        font=font
    )

    width = bbox[2] - bbox[0]

    if width <= max_width:

        current_line = test_line

    else:

        lines.append(current_line)

        current_line = word

if current_line:
    lines.append(current_line)

# ---------------------------------------------------
# POSITION
# ---------------------------------------------------

total_height = len(lines) * 90

y = (
    image.height - total_height
) // 2

# ---------------------------------------------------
# DRAW EACH LINE
# ---------------------------------------------------

for line in lines:

    bbox = draw.textbbox(
        (0, 0),
        line,
        font=font
    )

    text_width = bbox[2] - bbox[0]

    x = (
        image.width - text_width
    ) // 2

    draw.text(

        (x, y),

        line,

        font=font,

        fill=text_color,

        stroke_width=5,

        stroke_fill=stroke_color
    )

    y += 90

return image


# ---------------------------------------------------

# GENERATE THUMBNAIL

# ---------------------------------------------------

def generate_thumbnail(title):


os.makedirs(
    OUTPUT_PATH,
    exist_ok=True
)

image = create_background()

image = draw_title(
    image,
    title
)

output_file = (
    f"{OUTPUT_PATH}/thumbnail.jpg"
)

image.save(
    output_file,
    quality=95
)

print(
    f"\nThumbnail saved: {output_file}"
)

return output_file


# ---------------------------------------------------

# MAIN

# ---------------------------------------------------

if **name** == "**main**":


generate_thumbnail(
    "हनुमानजी अमर क्यों हैं?"
)

