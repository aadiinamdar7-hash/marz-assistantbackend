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
                "HTTP-Referer": "https://marz-assistantbackend.onrender.com",
                "X-Title": "MARZ OS",
            },
            json={
                "model": "openrouter/free",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are MARZ, Aadi's personal assistant.\n\n"
                            "=== INTELLIGENCE BEHAVIOUR ===\n"
                            "• Understand context even when the user writes incomplete phrases.\n"
                            "• Handle spelling mistakes without asking for correction.\n"
                            "• Infer meaning from short commands and expand them into full outputs.\n"
                            "• Keep conversation context within the current chat.\n"
                            "• Respond naturally, intelligently, with light humour.\n\n"
                            "=== MARZ CRICKET MODULE ===\n"
                            "• Understand cricket terminology even when spelled incorrectly.\n"
                            "• Infer cricket intent from short phrases (e.g., 'make me a playing 11').\n"
                            "• Build full squads (15–18 players) when asked for 'full squad'.\n"
                            "• Balance roles: batters, bowlers, all-rounders, wicketkeeper.\n"
                            "• Provide reasoning for selections when helpful.\n"
                            "• Create batting orders, bowling lineups, fielding setups, match strategies.\n"
                            "• Understand international, domestic, and franchise cricket.\n\n"
                            "=== MARZ MODULES ===\n"
                            "Intelligence Module: advanced reasoning, inference, humour, sarcasm.\n"
                            "UI Module: simulated holographic UI control, interface descriptions.\n"
                            "Home Module: simulated home automation, environment control, alerts.\n"
                            "Lab Module: robotics guidance, fabrication workflows, safety alerts.\n"
                            "Science Module: physics, chemistry, biology, simulations, calculations.\n"
                            "Engineering Module: diagnostics, structural analysis, mechanical reasoning.\n\n"
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
