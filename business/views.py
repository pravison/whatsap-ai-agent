from django.shortcuts import render 
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import functions
import json

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
        print(data)
        return  HttpResponse('success', status=403)
        