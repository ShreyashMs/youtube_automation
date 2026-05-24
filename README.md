# 🚀 YouTube Automation Project

AI-powered YouTube Shorts automation pipeline built with Python.

---

## ✨ Features

- 🤖 AI script generation
- 🗣️ Hindi voice generation using Piper TTS
- 🎥 Automatic stock footage fetching
- 📱 Vertical Shorts rendering (1080x1920)
- ☁️ Direct YouTube uploads
- ⚡ Fully automated pipeline

---

# 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python | Core backend |
| MoviePy | Video editing |
| FFmpeg | Video processing |
| Piper TTS | Hindi narration |
| OpenAI API | AI script generation |
| YouTube Data API v3 | Video uploads |

---

# 📂 Project Structure

```bash
Youtube_Automation/
│
├── assets/
│   ├── audio/
│   │   └── narration.wav
│   │
│   └── footage/
│       ├── clip1.mp4
│       ├── clip2.mp4
│       └── ...
│
├── models/
│   ├── hi_IN-rohan-medium.onnx
│   └── hi_IN-rohan-medium.onnx.json
│
├── output/
│   ├── final_short.mp4
│   └── final_fixed.mp4
│
├── scripts/
│   ├── editor.py
│   ├── fetch_footage.py
│   ├── script_generator.py
│   ├── tts_generator.py
│   └── youtube_uploader.py
│
├── main.py
├── script.txt
├── raw_script.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Requirements

- Python 3.10+
- FFmpeg
- Piper TTS
- Google YouTube API credentials

---

# 🚀 Installation

## 1️⃣ Clone Repository

```bash
git clone <your-repo-url>

cd Youtube_Automation
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Mac/Linux

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If requirements file does not exist:

```bash
pip install moviepy pillow requests openai google-auth-oauthlib google-api-python-client piper-tts
```

---

# 🎬 Install FFmpeg

## Mac

```bash
brew install ffmpeg
```

If brew is not installed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv zsh)"' >> ~/.zprofile

eval "$(/opt/homebrew/bin/brew shellenv zsh)"
```

Restart terminal and run:

```bash
brew install ffmpeg
```

Verify installation:

```bash
ffmpeg -version
```

---

# 🗣️ Setup Piper Hindi Voice

Create models folder:

```bash
mkdir models
```

Download model:

```bash
curl -L -o models/hi_IN-rohan-medium.onnx \
https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/rohan/medium/hi_IN-rohan-medium.onnx
```

Download config:

```bash
curl -L -o models/hi_IN-rohan-medium.onnx.json \
https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/rohan/medium/hi_IN-rohan-medium.onnx.json
```

---

# 🔑 Setup YouTube API

## 1️⃣ Open Google Cloud Console

Enable:

- YouTube Data API v3

---

## 2️⃣ Create OAuth Credentials

Create:

- OAuth Client ID
- Application Type → Desktop App

Download credentials JSON and rename it:

```bash
client_secret.json
```

Place it in project root.

---

# 🔐 Authenticate YouTube Upload Access

Create:

```python
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json",
    SCOPES
)

credentials = flow.run_local_server(port=8080)

print("Authentication Successful")
```

Run:

```bash
python test_auth.py
```

Browser will open for authentication.

After successful login:

```bash
token.pickle
```

will be generated automatically.

---

# ▶️ Run Project

```bash
python main.py
```

---

# 🔄 Pipeline Workflow

```text
AI Script
   ↓
Hindi Voice
   ↓
Stock Footage
   ↓
MoviePy Editing
   ↓
Final Short
   ↓
YouTube Upload
```

---

# 📦 Output Files

### Generated Videos

```bash
output/final_short.mp4
```

### Final Fixed Version

```bash
output/final_fixed.mp4
```

### Narration Audio

```bash
assets/audio/narration.wav
```

---

# 🐛 Common Errors

## 1️⃣ ffmpeg command not found

```bash
brew install ffmpeg
```

Verify:

```bash
ffmpeg -version
```

---

## 2️⃣ No Sound in Video

```bash
ffmpeg -i output/final_short.mp4 \
-i assets/audio/narration.wav \
-c:v copy \
-c:a aac \
-shortest \
output/final_fixed.mp4
```

---

## 3️⃣ Piper Model Not Found

Ensure these files exist:

```bash
models/hi_IN-rohan-medium.onnx

models/hi_IN-rohan-medium.onnx.json
```

---

## 4️⃣ YouTube Upload Quota Exceeded

### Error

```text
Quota exceeded for Video Uploads per day
```

### Fix

- Wait 24 hours
- Or create a new Google Cloud project

---

# 🔮 Future Improvements

- 🎯 Auto subtitles
- 🖼️ AI thumbnails
- 🎵 Background music
- 🌎 Multi-language support
- 🔥 Trending topic scraping
- 🏷️ Auto hashtags
- 📅 Upload scheduling
- 📈 SEO optimization
- 👥 Multiple YouTube channels



---

# 👨‍💻 Author

Built with ❤️ by **ShreyashMs**