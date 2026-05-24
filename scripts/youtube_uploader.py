import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video():

    creds = None

    # Load saved token
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # First-time login
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json",
                SCOPES
            )

            creds = flow.run_local_server(port=8080)

        # Save token
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    youtube = build("youtube", "v3", credentials=creds)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "महाभारत का सबसे बड़ा रहस्य 😱 #shorts",

                "description": """
भारत के रहस्यमयी इतिहास की ऐसी और कहानियों के लिए चैनल RamLala10 ko subscribe करें।

#महाभारत
#रामायण
#इतिहास
#mythology
#shorts
                """,

                "tags": [
                    "महाभारत",
                    "रामायण",
                    "इतिहास",
                    "भारत",
                    "mythology",
                    "hindu",
                    "shorts"
                ],

                "categoryId": "22"
            },

            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        },

        media_body=MediaFileUpload(
            "output/final_short.mp4",
            chunksize=-1,
            resumable=True
        )
    )

    response = request.execute()

    print("\nUPLOAD SUCCESSFUL")
    print("Video ID:", response["id"])