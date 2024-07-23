from django.shortcuts import render 
from django.http import HttpResponse
from django.views.decorators.csrf import crsf_exempt
from . import functions
import json

# Create your views here.

def index(request):
    return render(request, 'index.html')

def send(request):
    phoneNumber= "0740562740"
    message= "how a you pravison"
    ans = functions.sendWhatsappMessage(phoneNumber, message)
    return ans

@crsf_exempt
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
        return  HttpResponse('success', status=403)
        