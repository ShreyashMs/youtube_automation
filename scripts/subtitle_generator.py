import re
import math

# ---------------------------------------------------
# CLEAN TEXT
# ---------------------------------------------------

def clean_text(text):

    text = text.replace("\n", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()

# ---------------------------------------------------
# SPLIT LONG SENTENCES
# ---------------------------------------------------

def split_long_sentence(sentence):

    words = sentence.split()

    chunks = []

    current = []

    for word in words:

        current.append(word)

        # keep subtitle readable
        if len(current) >= 5:

            chunks.append(
                " ".join(current)
            )

            current = []

    if current:

        chunks.append(
            " ".join(current)
        )

    return chunks

# ---------------------------------------------------
# FORMAT TIME
# ---------------------------------------------------

def format_time(seconds):

    milliseconds = int(
        (seconds % 1) * 1000
    )

    seconds = int(seconds)

    mins = seconds // 60
    secs = seconds % 60

    return (
        f"{mins:02d}:{secs:02d},{milliseconds:03d}"
    )

# ---------------------------------------------------
# GENERATE SUBTITLES
# ---------------------------------------------------

def generate_subtitles(duration):

    with open(
        "script.txt",
        "r",
        encoding="utf-8"
    ) as f:

        script = f.read()

    script = clean_text(script)

    # ---------------------------------------------------
    # SPLIT INTO SENTENCES
    # ---------------------------------------------------

    sentences = re.split(

        r"(?<=[।!?])",

        script
    )

    sentences = [

        s.strip()

        for s in sentences

        if s.strip()
    ]

    # ---------------------------------------------------
    # SMALLER READABLE CHUNKS
    # ---------------------------------------------------

    final_lines = []

    for sentence in sentences:

        if len(sentence.split()) > 6:

            parts = split_long_sentence(
                sentence
            )

            final_lines.extend(parts)

        else:

            final_lines.append(sentence)

    # ---------------------------------------------------
    # TIMING
    # ---------------------------------------------------

    total_lines = max(
        len(final_lines),
        1
    )

    min_duration = 1.6

    subtitle_duration = max(

        duration / total_lines,

        min_duration
    )

    subtitles = []

    current_time = 0

    for line in final_lines:

        end_time = (
            current_time
            + subtitle_duration
        )

        subtitles.append({

            "start": round(current_time, 2),

            "end": round(end_time, 2),

            "text": line
        })

        current_time = end_time

    # ---------------------------------------------------
    # FIX OVERFLOW
    # ---------------------------------------------------

    if subtitles:

        subtitles[-1]["end"] = duration

    return subtitles

# ---------------------------------------------------
# GENERATE SRT FILE
# ---------------------------------------------------

def save_srt(subtitles, output="subtitles.srt"):

    with open(
        output,
        "w",
        encoding="utf-8"
    ) as f:

        for index, sub in enumerate(
            subtitles,
            start=1
        ):

            start = format_time(
                sub["start"]
            )

            end = format_time(
                sub["end"]
            )

            text = sub["text"]

            f.write(f"{index}\n")
            f.write(
                f"{start} --> {end}\n"
            )
            f.write(f"{text}\n\n")

# ---------------------------------------------------
# TEST
# ---------------------------------------------------

if __name__ == "__main__":

    duration = 40

    subtitles = generate_subtitles(
        duration
    )

    save_srt(subtitles)

    print("\nGenerated subtitles.srt\n")

    for sub in subtitles[:5]:

        print(sub)