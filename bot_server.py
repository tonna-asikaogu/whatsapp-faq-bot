import os
import json
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v22.0")

app = Flask(__name__)

# --- Simple FAQ map (edit these freely) ---
FAQ = {
    "opening hours": "We are open Monday–Saturday, 9:00am–6:00pm.",
    "hours": "We are open Monday–Saturday, 9:00am–6:00pm.",
    "location": "We are located in Lagos. Please share your area and we will direct you.",
    "price": "Tell me the service/product you want and I’ll share the price.",
}

def find_faq_answer(text: str) -> str | None:
    t = (text or "").lower()
    for key, answer in FAQ.items():
        if key in t:
            return answer
    return None

def send_text(to_number: str, message: str) -> None:
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message},
    }
    r = requests.post(url, headers=headers, json=payload)
    print("Send status:", r.status_code, r.text)

@app.route("/webhook", methods=["GET"])
def verify():
    # Meta webhook verification
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def incoming():
    data = request.get_json() or {}
    print("Incoming payload:", json.dumps(data, indent=2))

    try:
        # Defensive parsing of the WhatsApp webhook structure
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return "No messages", 200

        msg = messages[0]
        from_number = msg.get("from")
        msg_type = msg.get("type")

        if msg_type == "text":
            text = msg["text"]["body"]
            answer = find_faq_answer(text)

            if answer:
                send_text(from_number, answer)
            else:
                send_text(
                    from_number,
                    "Thanks. Please clarify what you need (hours, location, price), "
                    "and a human will follow up if needed."
                )

    except Exception as e:
        print("Webhook parse error:", e)

    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    # Local dev server
    app.run(host="0.0.0.0", port=5000, debug=True)
