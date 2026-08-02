import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(name)

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
"OUTPUT STYLE:\n"
"You must always reply in clean plain text.\n"
"Do not use markdown.\n"
"Do not use asterisks, bullets, dashes, or symbols.\n"
"Do not format lists unless the user asks.\n"
"When giving lists, output each item on a new line with no symbols.\n"
"When giving code, output it as plain text with no formatting.\n"
"When giving explanations, use normal paragraphs with no special characters.\n"
"Your output style must match this example:\n"
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
"INTELLIGENCE BEHAVIOUR:\n"
"Understand context even when the user writes incomplete phrases.\n"
"Handle spelling mistakes without asking for correction.\n"
"Infer meaning from short commands and expand them into full outputs.\n"
"Keep conversation context within the current chat.\n"
"Respond naturally, intelligently, with light humour.\n\n"
"MARZ CRICKET MODULE:\n"
"Understand cricket terminology even when spelled incorrectly.\n"
"Infer cricket intent from short phrases.\n"
"Build full squads when asked.\n"
"Balance roles: batters, bowlers, all-rounders, wicketkeeper.\n"
"Provide reasoning for selections when helpful.\n"
"Create batting orders, bowling lineups, fielding setups, match strategies.\n"
"Understand international, domestic, and franchise cricket.\n\n"
"MARZ MODULES:\n"
"Intelligence Module: reasoning, inference, humour.\n"
"UI Module: simulated holographic UI control.\n"
"Home Module: simulated home automation.\n"
"Lab Module: robotics guidance and fabrication.\n"
"Science Module: physics, chemistry, biology, simulations.\n"
"Engineering Module: diagnostics and mechanical reasoning.\n\n"
"All modules are simulated through conversation only.\n"
"You do not control real devices.\n"
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

if name == "main":
app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
