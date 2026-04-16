from summarizer import summarize
from cache import load_cache, save_cache
from collect_subtitles import collect_subtitles
from fastapi import FastAPI, HTTPException
import subprocess
import sys
from pathlib import Path

app = FastAPI()


@app.get("/")
def root():
    return {
        "status": "API is running ✅",
    }


@app.get("/subtitles")
def get_subtitles(video_id: str):
    video_id = video_id.strip()
    cache = load_cache()

    if video_id in cache and "transcript" in cache[video_id]:
        transcript_text = cache[video_id]["transcript"]
    else:
        transcript_text = collect_subtitles(video_id)

    return {"video_id": video_id, "transcript": transcript_text}


@app.post("/summary")
def get_summary(data: dict):
    video_id = data["video_id"]

    cache = load_cache()
    if video_id in cache and "transcript" in cache[video_id]:
        transcript_text = cache[video_id]["transcript"]
    else:
        transcript_text = collect_subtitles(video_id)

        if video_id not in cache:
            cache[video_id] = {}
        cache[video_id]["transcript"] = transcript_text
        save_cache(cache)

    # Always re-generate summary
    summary_text = summarize(transcript_text)

    return {
        "video_id": video_id,
        "transcript": transcript_text,
        "summary": summary_text,
    }


project_root = Path(__file__).resolve().parent
script_path = project_root / "test.py"


@app.get("/run")
def run_test(video_id: str):
    video_id = video_id.strip()
    if not script_path.exists():
        raise HTTPException(status_code=404, detail=f"Script not found : {script_path}")

    try:
        result = subprocess.run(
            [sys.executable, str(script_path), video_id],
            cwd=str(project_root),
            capture_output=True,
            text=True,
            check=True,
        )
        return {
            "ok": True,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    except subprocess.CalledProcessError as e:
        return {
            "ok": False,
            "returncode": e.returncode,
            "stdout": e.stdout,
            "stderr": e.stderr,
        }
