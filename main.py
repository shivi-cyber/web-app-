import os
import json
import tempfile
import subprocess
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import anthropic

app = FastAPI(title="AttentionX API", description="AI-powered content repurposing engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

@app.get("/")
async def root():
    index = frontend_path / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return {"message": "AttentionX API is running!"}

@app.post("/api/analyze-transcript")
async def analyze_transcript(transcript: str = Form(...), video_duration: Optional[float] = Form(300.0)):
    """
    Main AI analysis endpoint.
    Takes a transcript and returns:
    - Best clip timestamps with hooks
    - Viral score for each clip
    - Caption suggestions
    - Emotional peak analysis
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

    prompt = f"""You are an expert social media content strategist and viral video editor.

Analyze this video transcript and find the TOP 5 most viral-worthy moments (clips of 45-90 seconds each).

TRANSCRIPT:
{transcript}

VIDEO DURATION: {video_duration} seconds

For each clip, provide:
1. Start time (in seconds from video start)
2. End time (in seconds) 
3. A viral "HOOK" headline (under 10 words, stop-the-scroll style)
4. Why this moment is emotionally powerful (1-2 sentences)
5. Viral score out of 10 (based on: emotional intensity, practical value, surprising insight, relatability)
6. 3 dynamic caption suggestions (short, punchy, under 8 words each)
7. Recommended platform: TikTok, Instagram Reels, YouTube Shorts, or LinkedIn

Return ONLY valid JSON in this exact format:
{{
  "clips": [
    {{
      "id": 1,
      "start_time": 45,
      "end_time": 105,
      "hook": "The ONE thing nobody tells you about success",
      "why_viral": "Speaker reveals a counterintuitive truth that challenges conventional wisdom",
      "viral_score": 8.5,
      "captions": ["Nobody talks about this", "This changed everything", "The hidden truth revealed"],
      "platform": "TikTok",
      "emotion": "surprise"
    }}
  ],
  "summary": "Brief summary of the full content in 2 sentences",
  "total_viral_potential": 8.2,
  "content_type": "Educational/Motivational/Story-driven"
}}

Make the hooks EXTREMELY compelling - they should make someone stop scrolling immediately."""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text
    # Clean up JSON if wrapped in markdown
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

    result = json.loads(raw)
    return JSONResponse(content=result)


@app.post("/api/generate-captions")
async def generate_captions(
    clip_text: str = Form(...),
    style: str = Form("punchy")
):
    """Generate dynamic karaoke-style captions for a clip"""
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

    prompt = f"""You are a viral caption writer for short-form video.

Generate word-by-word timed captions for this clip text, optimized for the "{style}" style.

CLIP TEXT: {clip_text}

Rules:
- Break into 2-4 word phrases for maximum readability
- Each phrase should appear on screen for 0.5-1.5 seconds
- Make key words ALL CAPS for emphasis
- Add "..." for dramatic pauses

Return ONLY valid JSON:
{{
  "captions": [
    {{"text": "this is", "start": 0.0, "end": 0.8}},
    {{"text": "INCREDIBLE", "start": 0.8, "end": 1.6}}
  ],
  "highlight_words": ["word1", "word2"],
  "caption_style": "bold_yellow"
}}"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

    return JSONResponse(content=json.loads(raw))


@app.post("/api/analyze-youtube")
async def analyze_youtube(url: str = Form(...)):
    """
    Analyze a YouTube video by URL.
    In production: use yt-dlp to download audio, then Whisper to transcribe.
    For demo: returns a mock analysis with the URL.
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

    # In production you'd do:
    # 1. yt-dlp to get audio: subprocess.run(["yt-dlp", "-x", "--audio-format", "mp3", url])
    # 2. Whisper to transcribe: openai.Audio.transcribe("whisper-1", audio_file)
    # 3. Pass transcript to analyze_transcript()

    # For hackathon demo - AI generates realistic mock data based on URL
    prompt = f"""Generate a realistic demo analysis for a YouTube video at: {url}

Imagine this is an educational/motivational video (lecture, podcast, or workshop).
Create 5 realistic viral clip recommendations as if you analyzed the real video.

Return ONLY valid JSON:
{{
  "video_title": "Realistic title based on URL context",
  "clips": [
    {{
      "id": 1,
      "start_time": 180,
      "end_time": 255,
      "hook": "Compelling hook headline under 10 words",
      "why_viral": "Why this moment would go viral (1-2 sentences)",
      "viral_score": 8.7,
      "captions": ["Caption 1", "Caption 2", "Caption 3"],
      "platform": "TikTok",
      "emotion": "surprise"
    }}
  ],
  "summary": "What this video is about in 2 sentences",
  "total_viral_potential": 8.5,
  "content_type": "Educational"
}}"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

    return JSONResponse(content=json.loads(raw))


@app.get("/health")
async def health():
    return {"status": "ok", "service": "AttentionX"}
