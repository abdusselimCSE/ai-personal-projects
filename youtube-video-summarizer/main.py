from summarizer import summarize
from cache import load_cache, save_cache
from collect_subtitles import collect_subtitles
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "status": "API is running ✅",
    }


@app.get("/subtitles/{video_id}")
def get_subtitles(video_id: str):
    transcript_text = collect_subtitles(video_id)
    return {
        "video_id": video_id,
        "transcript": transcript_text,
    }


@app.post("/summary")
def get_summary(data: dict):

    video_id = data["video_id"]
    cache = load_cache()

    if video_id in cache:
        if "summary" in cache[video_id]:
            return {
                "message": "Loaded summary from cache.",
                "summary": cache[video_id]["summary"],
            }

    transcript_text = collect_subtitles(video_id)

    summary_text = summarize(transcript_text)

    if video_id not in cache:
        cache[video_id] = {}

    cache[video_id]["transcript"] = transcript_text
    cache[video_id]["summary"] = summary_text
    save_cache(cache)

    return {
        "video_id": video_id,
        "transcript": transcript_text,
        "summary": summary_text,
    }
