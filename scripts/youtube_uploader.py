import os
import pickle
import re
import time

from googleapiclient.errors import (
    HttpError
)

from google_auth_oauthlib.flow import (
    InstalledAppFlow
)

from google.auth.transport.requests import (
    Request
)

from googleapiclient.discovery import (
    build
)

from googleapiclient.http import (
    MediaFileUpload
)

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

SCOPES = [

    "https://www.googleapis.com/auth/youtube.upload",

    "https://www.googleapis.com/auth/youtube.force-ssl"
]

TOKEN_FILE = "token.pickle"

CLIENT_SECRET_FILE = "client_secret.json"

DEFAULT_VIDEO_PATH = (
    "output/final_short.mp4"
)

DEFAULT_TAGS = [

    "महाभारत",
    "रामायण",
    "हनुमान",
    "शिव",
    "krishna",
    "hindu mythology",
    "ytshorts",
    "shorts",
]

# ---------------------------------------------------
# CLEAN TITLE
# ---------------------------------------------------

def clean_title(title):

    title = title.strip()

    title = re.sub(
        r"\s+",
        " ",
        title
    )

    if "#shorts" not in title.lower():

        title += " #shorts"

    return title[:100]

# ---------------------------------------------------
# AUTHENTICATE
# ---------------------------------------------------

def authenticate_youtube():

    creds = None

    if os.path.exists(TOKEN_FILE):

        with open(
            TOKEN_FILE,
            "rb"
        ) as token:

            creds = pickle.load(token)

    if not creds or not creds.valid:

        if (
            creds
            and creds.expired
            and creds.refresh_token
        ):

            creds.refresh(Request())

        else:

            flow = (
                InstalledAppFlow
                .from_client_secrets_file(
                    CLIENT_SECRET_FILE,
                    SCOPES
                )
            )

            creds = flow.run_local_server(
                port=8080
            )

        with open(
            TOKEN_FILE,
            "wb"
        ) as token:

            pickle.dump(creds, token)

    youtube = build(
        "youtube",
        "v3",
        credentials=creds
    )

    return youtube

# ---------------------------------------------------
# ADD VIDEO TO PLAYLIST
# ---------------------------------------------------

def add_video_to_playlist(

    video_id,

    playlist_id
):

    try:

        youtube = authenticate_youtube()

        youtube.playlistItems().insert(

            part="snippet",

            body={

                "snippet": {

                    "playlistId": playlist_id,

                    "resourceId": {

                        "kind": "youtube#video",

                        "videoId": video_id
                    }
                }
            }

        ).execute()

        print(
            f"\nVideo added to playlist: {playlist_id}"
        )

        return True

    except HttpError as e:

        print(f"\nError adding video to playlist: {e}")

        return False

# ---------------------------------------------------
# UPLOAD VIDEO
# ---------------------------------------------------

def upload_video(

    title,

    description,

    video_path=DEFAULT_VIDEO_PATH,

    tags=None,

    playlist_id=None
):

    if not os.path.exists(video_path):

        raise FileNotFoundError(
            f"Video not found: {video_path}"
        )

    youtube = authenticate_youtube()

    title = clean_title(title)

    if not tags:

        tags = DEFAULT_TAGS

    request = youtube.videos().insert(

        part="snippet,status",

        body={

            "snippet": {

                "title": title,

                "description": description,

                "tags": tags,

                "categoryId": "22"
            },

            "status": {

                "privacyStatus": "public",

                "selfDeclaredMadeForKids": False
            }
        },

        media_body=MediaFileUpload(

            video_path,

            chunksize=-1,

            resumable=True
        )
    )

    response = None

    print("\nUploading video...")

    while response is None:

        status, response = request.next_chunk()

        if status:

            progress = int(
                status.progress() * 100
            )

            print(
                f"Upload progress: {progress}%"
            )

            time.sleep(1)

    video_id = response.get("id")

    video_url = (
        f"https://youtube.com/shorts/{video_id}"
    )

    print("\nUPLOAD SUCCESSFUL")

    print(video_url)

    # Add to playlist if playlist_id provided
    if playlist_id:

        add_video_to_playlist(

            video_id,

            playlist_id
        )

    return {

        "video_id": video_id,

        "video_url": video_url
    }

# ---------------------------------------------------
# POST COMMENT
# ---------------------------------------------------

def post_comment(

    video_id,

    comment_text
):

    try:

        youtube = authenticate_youtube()

        youtube.commentThreads().insert(

            part="snippet",

            body={

                "snippet": {

                    "videoId": video_id,

                    "topLevelComment": {

                        "snippet": {

                            "textOriginal": comment_text
                        }
                    }
                }
            }

        ).execute()

        print("\nComment posted successfully!")

    except HttpError as e:

        print("\nComment posting failed")

        print(e)

