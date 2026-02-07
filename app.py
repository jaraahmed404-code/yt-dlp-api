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
    data = request.json or {}
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    filename = f"/tmp/{uuid.uuid4()}.mp4"

    cmd = [
        "yt-dlp",
        "-f", "mp4",
        "--no-playlist",
        "-o", filename,
        url
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600
        )
if result.returncode != 0:
    return jsonify({
        "error": "yt-dlp failed",
        "stderr": result.stderr,
        "stdout": result.stdout,
        "cmd": " ".join(cmd)
    }), 500

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Download timeout"}), 504

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "file": filename,
        "status": "done"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
