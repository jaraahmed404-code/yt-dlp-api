from fastapi import FastAPI
import yt_dlp
import os

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/info")
def info(url: str):
    ydl_opts = {"quiet": True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        data = ydl.extract_info(url, download=False)

    return {
        "title": data.get("title"),
        "duration": data.get("duration"),
        "formats": len(data.get("formats", [])),
        "thumbnail": data.get("thumbnail"),
    }


@app.post("/download")
def download(data: dict):
    url = data["url"]

    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        "format": "best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return {"status": "ok"}
