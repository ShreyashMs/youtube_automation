# 🚀 YouTube Automation Project

JSON-authored YouTube Shorts pipeline built with Python. Each episode supplies its own Hindi script, metadata, hashtags, comment, and visual prompts; the pipeline creates narration, fetches fresh stock footage, renders the video, and uploads it with analytics tracking.

---

## ✨ Features

- 🗂️ **JSON-First Content** - Scripts, metadata, hashtags, comments, and visuals stay in versionable JSON files
- 🗣️ **Hindi Voice Generation** - Piper TTS for natural Hindi narration
- 🎥 **Stock Footage Fetching** - Automatic video clip acquisition
- 📱 **Vertical Shorts Rendering** - Optimized 1080x1920 format for YouTube Shorts
- ☁️ **Direct YouTube Uploads** - Automated video publishing with metadata
- 🎨 **AI Thumbnails** - Auto-generated custom thumbnails
- 💬 **Auto Comments** - Generate and post engaging comments on videos
- 📝 **Subtitles** - Support for subtitle generation
- 📊 **Analytics Tracking** - Save video metadata and performance data
- ⏰ **Upload Scheduling** - Schedule videos for future publishing
- 🏷️ **Metadata Generation** - Auto-generate titles and descriptions
- ⚡ **Fully Automated Pipeline** - End-to-end automation from script to upload

---

# 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python 3.10+ | Core backend |
| MoviePy | Video editing & composition |
| FFmpeg | Video processing & encoding |
| Piper TTS | Hindi voice synthesis |
| OpenAI API | AI script & comment generation |
| YouTube Data API v3 | Video uploads & publishing |
| Pillow | Image processing & thumbnails |
| Requests | HTTP client for API calls |

---

# 📂 Project Structure

```bash
Youtube_Automation/
│
├── assets/
│   ├── audio/
│   │   └── narration.wav
│   ├── fonts/
│   ├── footage/
│   │   └── (downloaded video clips)
│   ├── images/
│   ├── models/
│   │   ├── hi_IN-rohan-medium.onnx
│   │   └── hi_IN-rohan-medium.onnx.json
│   ├── music/
│   └── subtitles/
│
├── output/
│   ├── final_short.mp4
│   ├── final_fixed.mp4
│   └── thumbnail.jpg
│
├── scripts/
│   ├── analytics_tracker.py          # Save video analytics & metadata
│   ├── comment_generator.py          # Generate AI-powered comments
│   ├── config.py                     # Configuration settings
│   ├── content_patterns.py           # Content pattern definitions
│   ├── editor.py                     # MoviePy video editing logic
│   ├── fetch_footage.py              # Download stock footage
│   ├── logger.py                     # Logging utilities
│   ├── metadata_generator.py         # Generate titles & descriptions
│   ├── scheduler.py                  # Schedule video uploads
│   ├── script_generator.py           # Generate scripts via OpenAI
│   ├── subtitle_generator.py         # Create subtitle files
│   ├── thumbnail_generator.py        # Create video thumbnails
│   ├── topic_categories.py           # Topic category definitions
│   ├── topic_engine.py               # Topic management engine
│   ├── tts_generator.py              # Piper TTS voice generation
│   ├── visual_prompt_generator.py    # Generate visual descriptions
│   └── youtube_uploader.py           # YouTube API upload handler
│
├── main.py                           # Main pipeline orchestrator
├── requirements.txt                  # Python dependencies
├── script.txt                        # Generated script output
├── raw_script.txt                    # Raw script before processing
├── video_metadata.txt                # Video metadata cache
├── analytics.json                    # Video analytics data
├── client_secret.json                # YouTube API credentials
├── README.md
└── .gitignore
```

---

# ⚙️ Requirements

- Python 3.10+
- FFmpeg
- Piper TTS
- Google YouTube API credentials (OAuth 2.0)

---

# 🚀 Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/ShreyashMs/youtube_automation.git
cd Youtube_Automation
```

---

## 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
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

### Dependencies Included:

- moviepy (1.0.3)
- pillow
- requests
- python-dotenv
- google-auth-oauthlib
- google-api-python-client
- google-auth-httplib2
- numpy
- imageio & imageio-ffmpeg
- proglog, decorator, tqdm

---

# 🎬 Install FFmpeg

## Mac (Homebrew)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add Homebrew to PATH
echo 'eval "$(/opt/homebrew/bin/brew shellenv zsh)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv zsh)"

# Install FFmpeg
brew install ffmpeg

# Verify installation
ffmpeg -version
```

## Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install ffmpeg
ffmpeg -version
```

## Windows

Download from: https://ffmpeg.org/download.html or use:

```bash
choco install ffmpeg
```

---

# 🗣️ Setup Piper Hindi Voice Model

### Step 1: Create Models Directory

```bash
mkdir -p models
```

### Step 2: Download ONNX Model

```bash
curl -L -o models/hi_IN-rohan-medium.onnx \
https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/rohan/medium/hi_IN-rohan-medium.onnx
```

### Step 3: Download Model Config

```bash
curl -L -o models/hi_IN-rohan-medium.onnx.json \
https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/rohan/medium/hi_IN-rohan-medium.onnx.json
```

### Verify Files

```bash
ls -la models/
# Should show both .onnx and .onnx.json files
```

---

# 🔑 Setup YouTube API & Authentication

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **YouTube Data API v3**

## Step 2: Create OAuth Credentials

1. Go to **Credentials** → **Create Credentials**
2. Select **OAuth Client ID**
3. Choose **Desktop Application**
4. Download the credentials JSON file

## Step 3: Setup Credentials

1. Rename downloaded file to `client_secret.json`
2. Place it in the project root directory:

```bash
Youtube_Automation/
├── client_secret.json
├── main.py
└── ...
```

## Step 4: Authenticate

First run will prompt browser authentication:

```bash
python main.py
```

After login, `token.pickle` will be generated automatically for future runs.

---

# 🔐 Setup Environment Variables

Create a `.env` file in the project root:

```bash
PEXELS_API_KEY=your_pexels_key_here
```

---

# ▶️ Run the Complete Pipeline

```bash
python main.py
```

### JSON content format

`python main.py` reads the general queue in `assets/content_queue.json`; it does not run the Bhagwat Gita series. Add each new item to that file with its `id`, `title`, `script`, `description`, `hashtags`, `comment`, `visuals`, `emotion`, `music`, `subtitles`, and `voice`.

The pipeline reads no runtime AI-generated script, metadata, comment, or visual prompt. It claims an item before work begins, marks it complete only after a successful YouTube upload, and records Pexels video IDs in `data/used_footage.json` to avoid reusing clips. Completion state is stored in `data/content_queue_progress.json`.

Voice profiles are defined in `assets/voice_profiles.json`. `hindi_rohan` is the only model currently installed. To add another Piper voice, place its `.onnx` and matching `.onnx.json` files under `assets/models/`, add its model path under `voices`, and use that voice name in the queue item.

### What Happens:

1. Loads and claims the next uncompleted JSON queue item
2. Saves its narration and creates its thumbnail
3. Fetches new footage using its JSON visual prompts
4. Creates Hindi narration and renders the Short
5. Uploads the JSON title, description, hashtags, and comment
6. Marks the episode complete and saves analytics

---

# 🔄 Pipeline Workflow

```
┌─────────────────────┐
│ Load JSON Episode   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ JSON Metadata       │ (title, description, hashtags)
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│Generate Thumbnail   │ (AI-powered design)
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Fetch Stock        │ (Download video clips)
│   Footage           │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Generate Voice      │ (Piper TTS - Hindi)
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Create Video       │ (MoviePy editing)
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Upload to YouTube   │ (YouTube Data API)
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│Post Auto Comment    │ (AI-generated)
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│Save Analytics       │ (Track metadata)
└─────────────────────┘
```

---

# 📦 Output Files

After running the pipeline, check these output locations:

| File | Location | Purpose |
|------|----------|---------|
| Final Video | `output/final_short.mp4` | Ready-to-upload Shorts video |
| Thumbnail | `output/thumbnail.jpg` | Video thumbnail image |
| Audio | `assets/audio/narration.wav` | Hindi voice narration |
| Script | `script.txt` | Generated script text |
| Metadata | `video_metadata.txt` | Title, description, tags |
| Analytics | `analytics.json` | Video upload data & metrics |

---

# 🎯 Core Modules

## `script_generator.py`
Generates engaging scripts using OpenAI API with topic-based content patterns.

## `metadata_generator.py`
Creates titles and descriptions optimized for YouTube SEO.

## `tts_generator.py`
Converts text to Hindi speech using Piper TTS engine.

## `fetch_footage.py`
Downloads stock video clips from multiple sources based on script content.

## `editor.py`
Uses MoviePy to compose final video with clips, audio, text overlays, and effects.

## `thumbnail_generator.py`
Generates custom thumbnails with text and imagery.

## `youtube_uploader.py`
Handles YouTube API authentication and video publishing.

## `comment_generator.py`
Generates and posts engaging comments on uploaded videos.

## `analytics_tracker.py`
Saves video metadata and tracks performance metrics.

## `subtitle_generator.py`
Creates subtitle files for accessibility.

## `scheduler.py`
Schedules videos for future publishing.

---

# 🐛 Troubleshooting

## 1️⃣ FFmpeg Command Not Found

```bash
# Mac
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg

# Verify
ffmpeg -version
```

---

## 2️⃣ YouTube Authentication Failed

- Delete `token.pickle` if it exists
- Re-run `python main.py` to re-authenticate
- Ensure `client_secret.json` is in project root
- Check if YouTube API is enabled in Google Cloud Console

---

## 3️⃣ Piper Model Not Found

Ensure these files exist:

```bash
models/hi_IN-rohan-medium.onnx
models/hi_IN-rohan-medium.onnx.json
```

If missing, re-download them:

```bash
mkdir -p models
curl -L -o models/hi_IN-rohan-medium.onnx \
https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/rohan/medium/hi_IN-rohan-medium.onnx

curl -L -o models/hi_IN-rohan-medium.onnx.json \
https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/rohan/medium/hi_IN-rohan-medium.onnx.json
```

---

## 4️⃣ No Sound in Video

```bash
# Re-merge audio with video using FFmpeg
ffmpeg -i output/final_short.mp4 \
-i assets/audio/narration.wav \
-c:v copy \
-c:a aac \
-shortest \
output/final_fixed.mp4
```

---

## 5️⃣ YouTube Upload Quota Exceeded

```
Error: Quota exceeded for Video Uploads per day
```

**Solutions:**
- Wait 24 hours for quota to reset
- Create a new Google Cloud project with fresh quotas
- Upgrade to Google Cloud paid account for higher limits

---

## 6️⃣ OpenAI API Key Missing

Create `.env` file:

```bash
OPENAI_API_KEY=your_key_here
```

Get your key from: https://platform.openai.com/api-keys

---

# 🔮 Future Improvements

- 🎯 Advanced subtitle styling
- 🖼️ Multi-language thumbnail generation
- 🎵 Automatic background music mixing
- 🌎 Multi-language script generation
- 🔥 Real-time trending topic scraping
- 🏷️ Automatic hashtag optimization
- 📅 Advanced upload scheduling
- 📈 SEO optimization engine
- 👥 Multi-channel management
- 📊 Real-time analytics dashboard
- 🤖 Feedback loop for content improvement
- ⚡ Batch video processing

---

# 📝 Configuration

Edit `scripts/config.py` to customize:

- Video dimensions (1080x1920)
- Footage duration ranges
- Font sizes and styles
- Audio quality
- API endpoints
- Content categories

---

# 🤝 Contributing

Feel free to fork, modify, and improve this project!

---

# ⚠️ Legal Notice

- Ensure you have rights to all content used
- Respect copyright laws for stock footage
- Follow YouTube Community Guidelines
- Obtain necessary API permissions
- Comply with local broadcasting regulations

---

# 📄 License

This project is provided as-is for educational and personal use.

---

# 👨‍💻 Author

Built with ❤️ by **ShreyashMs**

For questions or issues, open an issue on GitHub.

---

**Last Updated:** June 2026
**Python Version:** 3.10+
**Status:** ✅ Active Development
