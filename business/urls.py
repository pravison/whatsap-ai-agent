from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('02a10962-b38b-4d7a-a62c-4f22e2a32e46/', views.whatsappWebhook, name='whatsapp-webhook'),
    path('send/', views.send, name='send'),
]

#webhook token 
#3611bd62-b967-4c49-8817-fadd7a6eea2c