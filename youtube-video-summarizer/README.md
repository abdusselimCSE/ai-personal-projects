# 🎥 YouTube Video Summarizer (NLP)

A Python-based FastAPI application that fetches YouTube subtitles (transcripts) via a RapidAPI endpoint, caches transcripts and summaries in `cache.json`, and generates an **extractive summary** using NLTK word-frequency scoring.

---

## ✅ What This Project Does

Given a YouTube **video_id**, the system:

1. Fetches subtitles from RapidAPI (or loads from cache if available)
2. Builds a clean transcript string
3. Summarizes the transcript using NLP (NLTK + frequency scoring)
4. Stores transcript and summary in `cache.json`
5. Exposes everything as REST API endpoints using FastAPI

---

## 📁 Project Structure

```text
youtube-video-summarizer/
├── main.py
├── collect_subtitles.py
├── summarizer.py
├── cache.py
├── cache.json
├── test.py
└── README.md
```

---

## ⚙️ Environment Setup

### 1) Install Dependencies

```bash
pip install fastapi uvicorn nltk python-dotenv requests
```

### 2) Environment Variables

Create a `.env` file in the same folder as `collect_subtitles.py`:

```env
RAPIDAPI_HOST=your_rapidapi_host
RAPIDAPI_KEY=your_rapidapi_key
```

If `RAPIDAPI_KEY` is missing, the application will raise an error.

---

## ▶️ Run the API Server

Run the server **from inside the project folder**:

```bash
cd youtube-video-summarizer
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

---

## 🌐 API Endpoints

### Health Check

**GET /**

```json
{
  "status": "API is running ✅"
}
```

---

### Get Subtitles

**GET /subtitles/{video_id}**

Example:

```
/subtitles/mBnqrlLnCCY
```

---

### Generate Summary

**POST /summary**

Request body:

```json
{
  "video_id": "mBnqrlLnCCY"
}
```

---

## 🔄 Internal Workflow

### collect_subtitles.py

- Fetches subtitles from RapidAPI
- Builds a clean transcript
- Saves transcript to cache

### cache.py

- Loads and saves cached transcripts/summaries
- Limits cache size automatically

### summarizer.py

- Cleans text
- Tokenizes sentences and words
- Removes stopwords
- Scores sentences
- Builds extractive summary

### main.py

- Exposes all functionality via FastAPI
- Handles caching logic

---

## 🧪 Testing

Start the server, then run:

```bash
python test.py
```

---

## 👤 Author

**Abdusselim**  
GitHub: https://github.com/abdusselimCSE
