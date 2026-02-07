from flask import Flask, request, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "YT-DLP API OK"

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    filename = f"/tmp/{uuid.uuid4()}.mp4"

    cmd = ["yt-dlp", "-f", "mp4", "-o", filename, url]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Download failed"}), 500

    return jsonify({
        "file": filename,
        "status": "done"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
