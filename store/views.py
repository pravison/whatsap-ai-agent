from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import CompanyInformation, Whatsapp
from customers.models import Customer, CustomerHistory, Order, OrderItem
from ai.models import Escalation
from .models import Product 
from customers.utils import cartData
# Create your views here.
def products(request):
    phone_number = request.session.get('phone_number')
    if phone_number:
        try:
            customer = Customer.objects.filter(phone_number=phone_number).first()
        except Customer.DoesNotExist:
            customer = Customer.objects.create(phone_number=phone_number)
            
        company = CompanyInformation.objects.order_by('id').first()
        title = company.company_name if company else "Your Site"
        whatsapp = Whatsapp.objects.order_by('id').first()
        products = Product.objects.all().order_by('-id')
        
        order =Order.objects.filter(customer=customer, complete=False).first()
        cartItems = OrderItem.objects.filter(order=order)
        context={
            'title': title,
            'products': products,
            'whatsapp': whatsapp,
            'cartItems': cartItems,
            'order': order
        }
        return render(request, 'products.html', context)
    else:
        return redirect('request_access')
    

def product(request, id ):
    phone_number = request.session.get('phone_number')
    if phone_number:
        try:
            customer = Customer.objects.filter(phone_number=phone_number).first()
        except Customer.DoesNotExist:
            customer = Customer.objects.create(phone_number=phone_number)
        company = CompanyInformation.objects.order_by('id').first()
        whatsapp = Whatsapp.objects.order_by('id').first()
        title = company.company_name if company else "Your Site"
        product = Product.objects.filter(id=id).first()
        # everytime customer visits this page we add it as a history
        CustomerHistory.objects.create( customer=customer, product=product)
        order =Order.objects.filter(customer=customer, complete=False).first()
        cartItems = OrderItem.objects.filter(order=order)
        context={
            'title': title,
            'company' : company,
            'product': product,
            'whatsapp': whatsapp,
            'cartItems': cartItems,
            'order': order
        }
        return render(request, 'product.html', context)
    else:
        return redirect('request_access')
    

def customer_escalations(request, id):
    phone_number = request.session.get('phone_number')
    if phone_number:
        try:
            customer = Customer.objects.filter(phone_number=phone_number).first()
        except Customer.DoesNotExist:
            customer = Customer.objects.create(phone_number=phone_number)
    else:
        return redirect('request_access')
    
    if customer:
        product = Product.objects.filter(id=id).first()
        messages.success(request, 'an attendand is coming to assist you')
        escalate, created = Escalation.objects.get_or_create(customer=customer, reasons=f'customer needs help with {product.name}')

        return redirect('product', id)
    else:
        messages.success(request, 'there was an error! please reach out to the counter for help')
        return redirect('product', id)