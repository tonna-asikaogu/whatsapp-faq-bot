import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v22.0")

def send_whatsapp_message(to_number: str, message: str):
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    print("Status code:", response.status_code)
    print("Response:", response.text)


if __name__ == "__main__":
    # 🔴 IMPORTANT: replace this with YOUR WhatsApp number (international format)
    YOUR_PHONE_NUMBER = "+13656622161"

    send_whatsapp_message(
        YOUR_PHONE_NUMBER,
        "Hello 👋 This message was sent from my Python WhatsApp bot!"
    )
