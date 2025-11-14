import os
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

@app.route('/webhook', methods=['POST'])
def helius_webhook_handler():
    raw_data = request.json
    if DISCORD_WEBHOOK_URL:
        try:
            pretty_json = json.dumps(raw_data, indent=2)
            message_content = "```json\n" + (pretty_json[:1900] + "\n... (truncated)" if len(pretty_json) > 1900 else pretty_json) + "\n```"
            requests.post(DISCORD_WEBHOOK_URL, json={"content": message_content})
        except Exception as e:
            requests.post(DISCORD_WEBHOOK_URL, json={"content": f"Error: {e}"})
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))