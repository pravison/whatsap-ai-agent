from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('product/<int:id>/', views.product, name='product'),
    path('asking-for-help/<int:id>/', views.customer_escalations, name='asking_for_help'),
]