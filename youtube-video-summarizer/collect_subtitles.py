from cache import load_cache, save_cache
import requests  # type: ignore
import os
from dotenv import load_dotenv
import json

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
    
    if response.status_code != 200:
        raise ValueError (f"RapidAPI error {response.status_code} : {response.text[:300]}")
    data = response.json()
    
    data = response.json()

    # Sometimes API returns JSON-as-string
    if isinstance(data, str):
        data = json.loads(data)

    # Validate expected structure
    if (
        not isinstance(data, dict)
        or "data" not in data
        or not isinstance(data["data"], dict)
        or "transcripts" not in data["data"]
    ):
        raise ValueError(f"Unexpected response shape: {str(data)[:300]}")

    transcripts = data["data"]["transcripts"]



    subtitles = None

    if "en_auto" in transcripts:
        subtitles = transcripts["en_auto"]["default"]

    if subtitles is None:
        if "en" in transcripts:
            subtitles = transcripts["en"]["default"]

    if subtitles is None:
        keys = list(transcripts.keys())

        if len(keys) > 0:
            first_key = keys[0]
            subtitles = transcripts[first_key]["default"]

    if subtitles is None:
        return ""

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
