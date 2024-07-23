from django.shortcuts import render
from . import functions

# Create your views here.

def index(request):
    return render(request, 'index.html')

def send(request):
    phoneNumber= "0740562740"
    message= "how a you pravison"
    ans = functions.sendWhatsappMessage(phoneNumber, message)
    return ans
