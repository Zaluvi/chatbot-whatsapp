from fastapi import FastAPI, Request
import requests
from twilio.rest import Client
import os

app = FastAPI()

# Variables de entorno (serán configuradas en Railway)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

# Configuración de Twilio
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Función para obtener respuesta de ChatGPT
def get_chatgpt_response(message):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4-turbo",
        "messages": [{"role": "user", "content": message}]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

# Webhook de WhatsApp
@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    data = await request.form()
    mensaje = data.get("Body")
    numero = data.get("From")

    respuesta = get_chatgpt_response(mensaje)

    client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=respuesta,
        to=numero
    )

    return {"status": "success"}
