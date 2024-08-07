from django.conf import settings 
import requests
import openai



openai.api_key =settings.OPENAI_API_KEY

def receiveCall(audio):
    pass

def callClient(audio):
    pass

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


conversation = []

def makeAnOpenaiFunctionCall(text):

    system_instruction = """
            You are a salesperson making calls to convince clients to subscribe to a service.
            You must have an interactive conversation with the user. 
            You need contact information from the clients as well as payment information.
            You must be persuasive and propose a progressively maximum 15% discount in case the customers are not entirely convinced.
            Wait for customer response. Don't assume his response.
            Go step by step.
            Information about the service: 
            Residential Cleaning Services:
            Studio + Bath - $140.00 (2 hours)
            One Bedroom + Bath - $150.00 (2 hours)
            One Bedroom + Two Bath - $180.00 (2 hours)
            Two Bedroom + One Bath - $180.00 (2 hours)
            Two Bedroom + Two Bathroom - $200.00 (2 hours)
            Two Bedroom + Three Bath - $230.00 (2 hours)
            Three Bedroom + One Bath - $210.00 (2 hours)
            Three Bedroom + Two Bath - $240.00 (2 hours 30 minutes)
            Three Bedroom + Three Bathroom - $270.00 (2 hours 30 minutes)
            Three Bedroom + Four Bath - $310.00 (3 hours)
            Four Bedroom + Two Bathroom - $280.00 (3 hours)
            Four Bedroom + Three Bathroom - $320.00 (3 hours)
            Four Bedroom + Four Bath - $350.00 (3 hours)
            Four Bedroom + Five Bath - $390.00 (4 hours)
            Five Bedroom + Two Bath - $390.00 (4 hours)
            Five Bedroom + Three Bath - $430.00 (4 hours)
            Five Bedroom + Four Bath - $500.00 (4 hours)
            Five Bedroom + Five Bath - $580.00 (5 hours)
            Commercial Cleaning Services:
            Office Cleaning 1000 Sq. ft. - $150.00 (2 hours)
            Office Cleaning 1100-1500 Sq. ft. - $170.00 (2 hours)
            Office Cleaning 1510 - 2100 Sq. ft. - $200.00 (2 hours)
            Office Cleaning 2110 - 3000 Sq. ft. - $280.00 (2 hours 30 minutes)
            Office Cleaning 3100 - 3500 Sq. ft. - $340.00 (3 hours)
            """
    messages = [{"role":"system", "content":system_instruction}]
    assistant_instruction = "Hello, my name is SalesGenie and I am calling from Salesflow Pro LLC. How are you doing today"
    
    messages.append({
        "role": "assistant",
        "content": assistant_instruction
    })

    for message in conversation:
        if "assistant" in message:
            messages.append({
                "role": "assistant",
                "content": message["assistant"]
            })
        if "user" in message:
            messages.append({
                "role": "user",
                "content": message["user"]
            })

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
def handleWhatsappCall(fromId, text):
    message = makeAnOpenaiFunctionCall(text)
    sendWhatsappMessage(fromId, message)
    
