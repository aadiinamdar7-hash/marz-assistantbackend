import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Your free-tier OpenRouter key
OPENROUTER_API_KEY = "freemodels"

# OpenRouter endpoint
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Free model router (automatically picks a free model)
MODEL = "openrouter/free"


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

                # REQUIRED for free-tier keys
                "HTTP-Referer": "https://your-frontend-domain.com",
                "X-Title": "MARZ OS",
            },
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are MARZ, Aadi's personal assistant. "
                            "You manage tasks, notes, reminders, study mode, "
                            "dev mode, diagnostics, and speak clearly."
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
        return jsonify({"reply": "MARZ backend error. Try again in a moment."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
