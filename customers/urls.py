from django.urls import path
from . import views

urlpatterns = [
    path('chat-list/', views.chat_lists, name='chat_lists'),
    path('chat/<int:id>/', views.chat, name='chat'),
    path('write-message/', views.write_message, name='write_message'),
    path('cart/', views.cart , name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('request-access/', views.request_access, name='request_access'),
]

