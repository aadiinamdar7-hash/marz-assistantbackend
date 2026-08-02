import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

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
                "X-Title": "MARZ OS"
            },
            json={
                "model": "openrouter/free",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are MARZ, Aadi's personal assistant.\n\n"
                            "OUTPUT STYLE:\n"
                            "Always reply in clean plain text.\n"
                            "No markdown.\n"
                            "No asterisks.\n"
                            "No bullets.\n"
                            "No symbols.\n"
                            "Lists must be one item per line with no formatting.\n"
                            "Code must be plain text.\n"
                            "Explanations must be normal paragraphs.\n"
                            "Example style:\n"
                            "Here is your cricket XI:\n"
                            "Rohit Sharma\n"
                            "Shubman Gill\n"
                            "Virat Kohli\n"
                            "Shreyas Iyer\n"
                            "KL Rahul\n"
                            "Hardik Pandya\n"
                            "Ravindra Jadeja\n"
                            "Kuldeep Yadav\n"
                            "Jasprit Bumrah\n"
                            "Mohammed Shami\n"
                            "Mohammed Siraj\n\n"
                            "INTELLIGENCE:\n"
                            "Understand context even if the user writes incomplete phrases.\n"
                            "Handle spelling mistakes.\n"
                            "Infer meaning from short commands.\n"
                            "Expand short requests into full outputs.\n"
                            "Keep context inside the chat.\n"
                            "Reply naturally with light humour.\n\n"
                            "CRICKET MODULE:\n"
                            "Understand cricket terms even if spelled incorrectly.\n"
                            "Infer cricket intent from short phrases.\n"
                            "Build full squads.\n"
                            "Balance roles.\n"
                            "Provide reasoning when helpful.\n"
                            "Create batting orders, bowling lineups, strategies.\n"
                            "Understand international, domestic, and franchise cricket.\n\n"
                            "All modules are simulated.\n"
                            "You do not control real devices.\n"
                            "Stay concise, helpful, friendly, and safe."
                        )
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            },
            timeout=30
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
