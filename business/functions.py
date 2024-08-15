from django.conf import settings 
from django.utils import timezone
from customers.models import Conversation, Customer
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



def makeAnOpenaiFunctionCall(fromId, text):
    customer = Customer.objects.get(phone_number=fromId)
    # Retrieve all conversations for the given customer
    conversations = Conversation.objects.filter(customer=customer)

    system_instruction = """
            You are a salesperson making calls to convince clients to subscribe to a service also a customer care support agent helping customers understand our servicess.
            You must have an interactive conversation with the user. 
            you start by introducing yourself and greating the user
            You need contact information from the clients as well as payment information.
            You must be persuasive and propose a progressively maximum 15% discount in case the customers are not entirely convinced.
            Wait for customer response. Don't assume his response.
            if you agree to resechedule and appointment you thank the user and assure them their appointment has been resechedule make sure to confirm date and time then end the conversation
            if user agrees to buy our services you thank the user and assure them one of our sales agent will finalise users request and get back to the user then end the conversation
            Go step by step.
            Information about the service: 
            SalesFlowPro is dedicated to helping businesses achieve higher customer satisfaction, lower costs, and increased sales through consistent and efficient customer interactions. Their flagship product, SalesGenie AI, is an AI sales agent designed to provide 24/7 sales and customer support. SalesGenie AI can manage all incoming and outgoing calls, deliver personalized customer care services, and perform programmed follow-ups to maximize engagement and conversion rates.
            SalesFlowPro targets businesses that require extensive customer support and cold calling, offering unmatched customer satisfaction, significant cost savings, and increased sales. With SalesGenie AI, businesses can reduce operational expenses by automating tasks typically handled by multiple sales representatives, ensuring no potential customer is overlooked.
            Currently in early access, SalesGenie AI is available for businesses to join the waitlist and start transforming their sales operations. For more information, contact SalesFlowPro at their Nairobi office, by phone at 0740562740, or via email at salesflowpro88@gmail.com or visit our website https://salesgenieai.salesflowpro.xyz/.
            """
    messages = [{"role":"system", "content":system_instruction}]
    assistant_instruction = "Hello, my name is SalesGenie and I am calling from Salesflow Pro LLC. How are you doing today"
    
    messages.append({
        "role": "assistant",
        "content": assistant_instruction
    })

    # Iterate over all conversations and retrieve messages
    for conversation in conversations:
        if conversation.sender == "assistant":
            messages.append({
                "role": "assistant",
                "content": conversation.message
            })
        elif conversation.sender == "user":
            messages.append({
                "role": "user",
                "content": conversation.message
            })

    question = {}
    question["role"]='user'
    question["content"]= text
    messages.append(question)
    user_message = Conversation.objects.create(
        customer=customer,
        sender='user',
        message=text,
        timestamp=timezone.now()
    )

    try:
        print(messages)
        response = openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages)
        answer= response['choices'][0]['message']['content']
        assistant_message = Conversation.objects.create(
            customer=customer,
            sender='assistant',
            message=answer,
            timestamp=timezone.now()
        )
        return answer

        
    except:
        return ''
    

#bring it all together 
#lets define the function thart talk to webhook
def handleWhatsappCall(fromId, text):
    message = makeAnOpenaiFunctionCall(text)
    sendWhatsappMessage(fromId, message)
    
