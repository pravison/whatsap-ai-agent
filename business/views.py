from django.shortcuts import render 
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .functions import sendWhatsappMessage, handleWhatsappCall
import json
from django.views.decorators.http import require_POST

from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(10)

# Create your views here.

def index(request):
    return render(request, 'index.html')



# @csrf_exempt
# @require_POST
# def whatsappWebhook(request):
#     if request.method == "GET":
#         VERIFY_TOKEN = "3611bd62-b967-4c49-8817-fadd7a6eea2c"
#         mode = request.GET['hub.mode']
#         token = request.GET['hub.verify_token']
#         challenge = request.GET['hub.challenge']

#         if mode == 'subscribe' and token == VERIFY_TOKEN:
#             return HttpResponse(challenge, status=200)
#         else:
#             return HttpResponse('error', status=403)
        
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         #print(data)
#         if 'object' in data and 'entry' in data:
#             if data['object'] == 'whatsapp_business_account':
#                 try:
#                     for entry in data['entry']:
#                         phoneId =  entry['changes'][0]['value']['metadata']['phone_number_id']
#                         profileName = entry['changes'][0]['value']['contacts'][0]['profile']['name']
#                         whatsAppId =  entry['changes'][0]['value']['contacts'][0]['wa_id']
#                         fromId =  entry['changes'][0]['value']['messages'][0]['from']
#                         text = entry['changes'][0]['value']['messages'][0]['text']['body']

#                         sendWhatsappMessage(fromId, f'AI is working on it ...')
#                         executor.submit( handleWhatsappCall, fromId , text)
                        
#                 except:
#                     pass
#             else:
#                 pass
#         else:
#             pass

#         return  HttpResponse('success', status=403)
        
@csrf_exempt
@require_POST
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
                        # contacts = value.get('contacts', [])
                        # if contacts:
                        #     profileName = contacts[0].get('profile', {}).get('name')
                        #     whatsAppId = contacts[0].get('wa_id')
                        messages = value.get('messages', [])
                        if messages:
                            fromId = messages[0].get('from')
                            text = messages[0].get('text', {}).get('body')

                            # Send the response once per incoming message
                            sendWhatsappMessage(fromId, f'AI 🧠 is working on it ...')
                            executor.submit( handleWhatsappCall, fromId , text)
                            break
            except Exception as e:
                print(f"Error processing webhook data: {e}")
                return HttpResponse('error', status=500)
        else:
            return HttpResponse('error', status=400)

        return HttpResponse('success', status=200)