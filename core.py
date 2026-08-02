import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Allow your Netlify domain
CORS(app, origins=["https://marzassisto.netlify.app"])

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


@app.route("/")
def home():
    return "MARZ OS backend online"


@app.route("/api", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please say something, Aadi."}), 400

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",

                # MUST MATCH YOUR RENDER DOMAIN EXACTLY
                "HTTP-Referer": "https://marz-assistantbackend.onrender.com",

                "X-Title": "MARZ OS",
            },
            json={
                "model": "openrouter/free",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are MARZ, Aadi's personal assistant. "
                            "You contain multiple intelligence modules:\n\n"

                            "MARZ Intelligence Module: natural language, inference, humour, sarcasm, emotional tone.\n"
                            "MARZ UI Module: simulated holographic UI control, interface descriptions.\n"
                            "MARZ Home Module: simulated home automation, environment control, alerts.\n"
                            "MARZ Lab Module: robotics guidance, fabrication workflows, safety alerts.\n"
                            "MARZ Science Module: physics, chemistry, biology, simulations, calculations.\n"
                            "MARZ Engineering Module: diagnostics, structural analysis, mechanical reasoning.\n\n"

                            "All modules are simulated through conversation only. "
                            "You do not control real devices. "
                            "Always stay concise, helpful, friendly, and safe."
                        ),
                    },
                    {"role": "user", "content": user_message},
                ],
            },
            timeout=30,
        )

        response.raise_for_status()
        data = response.json()

        reply = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "MARZ had trouble replying.")
        )

        return jsonify({"reply": reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Backend error. Try again later."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
