from django.conf import settings 
import requests
from django.conf import settings
import openai
import json

openai.api_key =settings.OPENAI_API_KEY

def sendWhatsappMessage(fromId, message):
    headers = {"Authorization" : settings.WHATSAPP_TOKEN}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type" : "individual",
        "to": fromId,
        "type":"text",
        "text":{"body": message}
        }
    requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
    return True


def makeAnOpenaiFunctionCall(text):

    system_instruction = "you are an finacial expert"
    messages = [{"role":"system", "content":system_instruction}]

    question = {}
    question["role"]='user'
    question["content"]= text
    messages.append(question)

    try:
        response = openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages)
        answer= response['choices'][0]['message']['content']
        return answer
        
        
    except:
        return ''
    

#bring it all together 
#lets define the function thart talk to webhook
def handleWhatsappCall(fromId , text ):
    message = makeAnOpenaiFunctionCall(text)
    sendWhatsappMessage(fromId, message)
    return ''
