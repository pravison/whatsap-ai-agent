from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('leads_warmup_page/', views.leadsWarmupPage, name='leads_warmup_page'),
    path('add_customer_to_pipeline/', views.addCustomersForFollowUp, name='add_customer_to_pipeline'),
    path('follow_up_customers/', views.customersForFollowUp, name='follow_up_customers'),
    path('policy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('02a10962-b38b-4d7a-a62c-4f22e2a32e46/', views.whatsappWebhook, name='whatsapp-webhook'),
]

