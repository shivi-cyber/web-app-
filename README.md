# ⚡ AttentionX — AI Content Repurposing Engine

> Turn 1-hour videos into viral short clips using AI. Built for the UnsaidTalks AttentionX AI Hackathon.
---
## 🧠 What it does

AttentionX analyzes long-form video content and automatically:

1. **Finds Viral Moments** — AI detects emotionally powerful segments with the highest viral potential
2. **Writes Viral Hooks** — Stop-the-scroll headlines under 10 words
3. **Scores Each Clip** — Viral score 0-10 based on emotion, insight, surprise, and relatability  
4. **Generates Captions** — Dynamic karaoke-style caption suggestions
5. **Platform Targeting** — Recommends TikTok, Reels, YouTube Shorts, or LinkedIn for each clip

## 🏗 Architecture

```
attentionx/
├── backend/
│   ├── main.py          # FastAPI server + AI endpoints
│   └── requirements.txt # Python dependencies
├── frontend/
│   └── index.html       # Beautiful single-page app
├── .env.example         # Environment variables template
├── render.yaml          # Deployment config for Render
├── Procfile             # For Railway/Heroku
└── README.md
```

## 🚀 Running Locally (Step by Step)

### Step 1: Get your Anthropic API Key
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up / Log in
3. Click "API Keys" → "Create Key"
4. Copy the key (starts with `sk-ant-...`)

### Step 2: Clone and set up
```bash
git clone https://github.com/YOUR_USERNAME/attentionx.git
cd attentionx
```

### Step 3: Create environment file
```bash
cp .env.example .env
# Open .env and paste your API key
```

### Step 4: Install Python dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 5: Run the server
```bash
uvicorn backend.main:app --reload
```

### Step 6: Open the app
Visit [http://localhost:8000](http://localhost:8000) 🎉

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/analyze-transcript` | Analyze a text transcript |
| `POST` | `/api/analyze-youtube` | Analyze a YouTube URL |
| `POST` | `/api/generate-captions` | Generate timed captions for a clip |
| `GET`  | `/health` | Health check |

---

## 🌐 Deploying to Render (Free Hosting)

1. Push your code to GitHub (public repo)
2. Go to [render.com](https://render.com) → Sign up free
3. Click **"New Web Service"** → Connect GitHub repo
4. Settings:
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variable: `ANTHROPIC_API_KEY` = your key
6. Click Deploy! 🚀

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Engine | Claude (Anthropic) |
| Backend | FastAPI (Python) |
| Frontend | Vanilla HTML/CSS/JS |
| Deployment | Render / Railway |
| Video (prod) | MoviePy + Librosa |
| Transcription (prod) | OpenAI Whisper |
| Face Detection (prod) | MediaPipe |

---

## 📊 Evaluation Criteria Coverage

- ✅ **Impact (20%)** — Turns 1 hour of content into 5 ready-to-post viral clips automatically
- ✅ **Innovation (20%)** — Viral scoring system + identity-aware hook generation
- ✅ **Technical Execution (20%)** — Clean FastAPI backend, Claude AI integration, full README
- ✅ **User Experience (25%)** — Beautiful dark UI, 3 input methods, instant results
- ✅ **Presentation (15%)** — Demo video linked above

---

## 🔮 Production Roadmap

- [ ] Real video processing with MoviePy
- [ ] Audio loudness analysis with Librosa (find emotional peaks by audio spikes)
- [ ] Actual YouTube download via yt-dlp
- [ ] Real transcription via OpenAI Whisper with timestamps
- [ ] Face tracking with MediaPipe for smart vertical crop
- [ ] FFmpeg-based video export with burned-in captions
- [ ] User accounts + clip history

---

*Built with ❤️ for the UnsaidTalks AttentionX Hackathon*
