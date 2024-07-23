from django.conf import settings 
import requests

phoneNumber = "0740562740"
message = "how are you pravison"

def sendWhatsappMessage(phoneNumber, message):
    headers = {"Authorization" : settings.WHATSAPP_TOKEN}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type" : "individual",
        "to": phoneNumber,
        "type":"text",
        "text":{"body": message}
        }
    response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
    ans= response.json()


