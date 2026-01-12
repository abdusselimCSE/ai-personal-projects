from cache import load_cache, save_cache
import requests  # type: ignore
import os
from dotenv import load_dotenv

load_dotenv()

x_rapidapi_host = os.getenv("RAPIDAPI_HOST")
x_rapidapi_key = os.getenv("RAPIDAPI_KEY")

if not x_rapidapi_key:
    raise ValueError("RPIDAPI_KEY not found. Put it in the .env file.")

def collect_subtitles(video_id):

    cache = load_cache()

    if video_id in cache:
        if "transcript" in cache[video_id]:
            print("Loading from cahce...")
            return cache[video_id]["transcript"]

    url = "https://youtube-video-summarizer-gpt-ai.p.rapidapi.com/api/v1/get-transcript-v2"

    querystring = {
        "video_id": video_id,
        "platform": "youtube",
        "format_subtitle": "srt",
        "format_answer": "json",
    }

    headers = {
        "x-rapidapi-host": x_rapidapi_host,
        "x-rapidapi-key": x_rapidapi_key,
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    subtitles = data["data"]["transcripts"]["en_auto"]["default"]

    all_subtitles = ""

    for item in subtitles:
        text = item["text"].strip()
        if len(text) > 0:
            all_subtitles = all_subtitles + text + "\n"

    transcript_text = all_subtitles.strip()

    # Save to cache
    if video_id not in cache:
        cache[video_id] = {}

    cache[video_id]["transcript"] = transcript_text
    save_cache(cache)

    print(f"Saved to cache for video id: {video_id}")
    return transcript_text
