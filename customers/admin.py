from django.contrib import admin
from . models import Customer, Conversation, CustomerHistory, Order, OrderItem
# Register your models here.
admin.site.register(Customer)
admin.site.register(Conversation)
admin.site.register(CustomerHistory)
admin.site.register(Order)
admin.site.register(OrderItem)
