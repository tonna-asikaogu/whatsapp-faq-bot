# WhatsApp FAQ Automation Bot

A WhatsApp chatbot built with Python and Flask using the WhatsApp Cloud API.
The bot automatically responds to common customer questions using webhook-based message handling.

## What this does
Small businesses often receive repetitive questions on WhatsApp (opening hours, location, pricing).
This project demonstrates how those queries can be handled automatically.

## How it works
1. A user sends a message to a WhatsApp number
2. Meta forwards the message to a Flask webhook
3. The backend parses the incoming text
4. Simple FAQ logic selects a response
5. The bot replies automatically via the WhatsApp Cloud API

## Tech stack
- Python
- Flask
- WhatsApp Cloud API
- Webhooks
- ngrok (local development)
- Requests

## Project status
This is a functional development prototype created for learning and portfolio demonstration.
It is not yet deployed as a permanent production service.
