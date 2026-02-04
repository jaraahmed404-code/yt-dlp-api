from flask import Flask, request, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")

    filename = f"/tmp/{uuid.uuid4()}.mp4"

    cmd = ["yt-dlp", "-f", "mp4", "-o", filename, url]
    subprocess.run(cmd, check=True)

    return jsonify({
        "file": filename,
        "status": "done"
    })

app.run(host="0.0.0.0", port=8080)
