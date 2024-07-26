from django.shortcuts import render 
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .functions import sendWhatsappMessage, handleWhatsappCall
import json

from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(1)

# Create your views here.

def index(request):
    return render(request, 'index.html')



@csrf_exempt
def whatsappWebhook(request):
    if request.method == "GET":
        VERIFY_TOKEN = "3611bd62-b967-4c49-8817-fadd7a6eea2c"
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse('error', status=403)
        
    if request.method == 'POST':
        data = json.loads(request.body)
        #print(data)
        if 'object' in data and 'entry' in data:
            if data['object'] == 'whatsapp_business_account':
                try:
                    for entry in data['entry']:
                        phoneNumber = entry['changes'][0]['value']['metadata']['display_phone_number']
                        phoneId =  entry['changes'][0]['value']['metadata']['phone_number_id']
                        profileName = entry['changes'][0]['value']['contacts'][0]['profile']['name']
                        whatsAppId =  entry['changes'][0]['value']['contacts'][0]['wa_id']
                        fromId =  entry['changes'][0]['value']['messages'][0]['from']
                        messageId = entry['changes'][0]['value']['messages'][0]['id']
                        timestamp = entry['changes'][0]['value']['messages'][0]['timestamp']
                        text = entry['changes'][0]['value']['messages'][0]['text']['body']

                        #handleWhatsappCall(fromId , text )
                        executor.submit( handleWhatsappCall, fromId , text)
                        # message = 'RE {} was received'.format(text)
                        # sendWhatsappMessage(fromId, message)
                        return ''
                except:
                    pass

        return  HttpResponse('success', status=403)
        