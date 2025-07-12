from flask import Flask, request, send_file, jsonify
import requests
import time
import os

app = Flask(__name__)

# Replace with your actual Stable Horde API Key
API_KEY = "4xvqgNbOCsy2FLbtZgUpzw"

# Simple static API key check (you can upgrade later)
VALID_KEYS = ["sukuna123", "ironman420"]

@app.route('/')
def home():
    return "🚀 Ironman AI Image Generator API is Live!"

@app.route('/generate', methods=['POST'])
def generate():
    # Auth check
    key = request.headers.get("Authorization", "").replace("Bearer ", "")
    if key not in VALID_KEYS:
        return jsonify({"error": "Unauthorized - Invalid API Key"}), 401

    # Prompt check
    prompt = request.json.get("prompt")
    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400

    # Request to Stable Horde
    headers = {
        "Client-Agent": "ironman-ai/1.0",
        "apikey": API_KEY
    }

    payload = {
        "prompt": prompt,
        "params": {
            "n": 1,
            "width": 512,
            "height": 512,
            "steps": 25
        },
        "nsfw": False,
        "censor_nsfw": True
    }

    try:
        res = requests.post("https://stablehorde.net/api/v2/generate/async", headers=headers, json=payload)
        job_id = res.json()["id"]

        # Wait for generation
        while True:
            time.sleep(5)
            check = requests.get(f"https://stablehorde.net/api/v2/generate/status/{job_id}")
            check_data = check.json()

            if check_data.get("done", False):
                img_url = check_data["generations"][0]["img"]
                img_data = requests.get(img_url).content

                # Save image
                with open("output.png", "wb") as f:
                    f.write(img_data)

                return send_file("output.png", mimetype='image/png')
            else:
                print("⏳ Still generating...")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
