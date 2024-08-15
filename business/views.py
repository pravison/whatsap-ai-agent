from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .functions import sendWhatsappMessage, handleWhatsappCall, callClient
from customers.models import Customer
import json


from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(10)

processed_message_ids = set()

def index(request):
    return render(request, 'index.html')

def terms(request):
    context = {
       
    }
    return render(request, 'terms.html', context)
def privacy(request):
    context = {
       
    }
    return render(request, 'policy.html', context)
        
@csrf_exempt
def whatsappWebhook(request):
    if request.method == "GET":
        VERIFY_TOKEN = "3611bd62-b967-4c49-8817-fadd7a6eea2c"
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse('error', status=403)
        
    if request.method == 'POST':
        data = json.loads(request.body)
        if 'object' in data and data['object'] == 'whatsapp_business_account':
            try:
                for entry in data.get('entry', []):
                    changes = entry.get('changes', [])
                    if changes:
                        value = changes[0].get('value', {})
                        # metadata = value.get('metadata', {})
                        # phoneId = metadata.get('phone_number_id')
                        contacts = value.get('contacts', [])
                        if contacts:
                            profileName = contacts[0].get('profile', {}).get('name')
                            # whatsAppId = contacts[0].get('wa_id')
                        messages = value.get('messages', [])
                        if messages:
                            fromId = messages[0].get('from')
                            text = messages[0].get('text', {}).get('body')
                            message_id = messages[0].get('id')

                            # Check if customer with the phone number exists
                            customer, created = Customer.objects.get_or_create(
                                phone_number=fromId,
                                defaults={
                                    'whatsapp_profile': profileName,
                                }
                            )

                            if created:
                                print(f"New customer added: {customer}")
                            else:
                                print(f"Customer already exists: {customer}")

                            # Process the message only if it hasn't been processed before
                            if message_id not in processed_message_ids:
                                # sendWhatsappMessage(fromId, text)
                                handleWhatsappCall(fromId , text)
                                processed_message_ids.add(message_id)
                                break
                            break
            except Exception as e:
                print(f"Error processing webhook data: {e}")
                return HttpResponse('error', status=500)
        else:
            return HttpResponse('error', status=400)

        return HttpResponse('success', status=200)
    


