from fastapi import FastAPI
import yt_dlp

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/info")
def info(url: str):
    ydl_opts = {}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return info


@app.post("/download")
def download(data: dict):
    url = data["url"]

    ydl_opts = {
        "format": "best",
        "outtmpl": "downloads/%(title)s.%(ext)s"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return {"status": "downloaded"}
