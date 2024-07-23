from django.shortcuts import render
from . import functions

# Create your views here.

def index(request):
    return render(request, 'index.html')


