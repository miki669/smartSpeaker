from flask import Flask, request, send_file, jsonify
import subprocess
import uuid
import os
import json

app = Flask(__name__)

MODEL = "models/denis.onnx"
CONFIG = "models/denis-onnx.json"
ESPEAK = "espeak-ng-data"
PIPER_BIN = "./piper"

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify(error="No text provided"), 400

    filename = f"out_{uuid.uuid4().hex}.wav"
    command = [
        PIPER_BIN,
        "--model", MODEL,
        "--config", CONFIG,
        "--espeak_data", ESPEAK,
        "--output_file", filename,
        "--json-input"
    ]

    try:
        result = subprocess.run(
            command,
            input=json.dumps({"text": text}),
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("[PIPER ERROR]", result.stderr)
            return jsonify(error="Piper execution failed", stderr=result.stderr), 500

        if not os.path.exists(filename):
            print("[PIPER WARNING] File not created:", filename)
            return jsonify(error="Piper did not create the output file"), 500

        return send_file(filename, mimetype="audio/wav")

    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
