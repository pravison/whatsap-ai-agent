from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Count, Q, Max, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import CompanyInformation, Whatsapp
from .models import Customer, Conversation, Order, OrderItem
from store.models import Product
from business.functions import sendWhatsappMessage
from django.utils import timezone
import json

# Create your views here.
@login_required
def chat_lists(request):
    company = CompanyInformation.objects.order_by('id').first()
    title = company.company_name if company else "Your Site"
    # get customers that have atleast one converstion
    # customers_with_converstaions = Customer.objects.filter(id__in=Conversation.objects.values('customer_id'))
    # customers_with_converstaions = Customer.objects.filter(conversations__isnull=False).distinct()
    customers = Customer.objects.annotate(unread_count=Count('conversations', filter=Q(conversations__read=False)), last_message_send=Max('conversations__timestamp')).order_by('-last_message_send')
    context = {
        'title': title,
        'company': company,
        'customers': customers
        # 'customers_with_converstaions' : customers_with_converstaions
    }
    return render(request, 'chats-lists.html', context)

@login_required
def chat(request, id):
    company = CompanyInformation.objects.order_by('id').first()
    title = company.company_name if company else "Your Site"
    customer = Customer.objects.filter(id=id).first()
    chats = Conversation.objects.filter(customer=customer).order_by('timestamp')

    chats.filter(sender="customer", read=False).update(read=True)
    if request.method == 'POST':
        message = request.POST['message']

        chat = Conversation(customer=customer, sender="AI", message=message, read=True)
        chat.save()
        # sending message throug whatsap
        fromId = customer.phone_number
        sendWhatsappMessage(fromId, message)
        messages.success(request, f'message send to {customer.name}')
        customer.last_talked = timezone.now().date()
        customer.save()
        return redirect('chat', customer.id)
    context = {
        'title': title,
        'company': company,
        'customer': customer,
        'chats': chats
    }
    return render(request, 'chat.html', context)

@login_required
def write_message(request):
    company = CompanyInformation.objects.order_by('id').first()
    customers = Customer.objects.all()
    title = company.company_name if company else "Your Site"
    if request.method == "POST":
        selected_customers = request.POST.getlist('customers')
        funnel_stage = request.POST.get('funnel_stage')
        message_template = request.POST.get('message')

        if funnel_stage:
            if funnel_stage == 'all':
                customers_to_receive_messages = Customer.objects.all()
            else:
                customers_to_receive_messages = Customer.objects.filter(funnel_stage=funnel_stage)
        else:
            # get selected customer 
            customers_to_receive_messages = Customer.objects.filter(id__in = selected_customers)
        for customer in customers_to_receive_messages:

            personalized_message = message_template.replace('{name}', customer.name)
            
            chat = Conversation(customer=customer, sender="AI", message=personalized_message, read=True)
            chat.save()
            customer.last_talked = timezone.now().date()
            customer.save()
            # sending message through whatsap
            fromId = customer.phone_number
            sendWhatsappMessage(fromId, personalized_message)
        messages.success(request, f'message send to selected customers')
        return redirect('write_message')
            
    
    
    context = {
        'title': title,
        'company': company,
        'customers' : customers
    }
    return render(request, 'write-message.html', context)

def cart(request):
    phone_number = request.session.get('phone_number')
    if phone_number:
        try:
            customer = Customer.objects.filter(phone_number=phone_number).first()
        except Customer.DoesNotExist:
            customer = Customer.objects.create(phone_number=phone_number)

        company = CompanyInformation.objects.order_by('id').first()
        title = company.company_name if company else "Your Site"
        order =Order.objects.filter(customer=customer, complete=False).first()
        cartItems = OrderItem.objects.filter(order=order)
        total_items = cartItems.count()
        context = {
        'order': order,
        'cartItems':cartItems,
        'company': company,
        'title' :title,
        'total_items': total_items
        }
        return render (request, 'cart.html', context)
    else:
        return redirect('request_access')
    
        
    

def checkout(request):
    phone_number = request.session.get('phone_number')
    if phone_number:
        try:
            customer = Customer.objects.filter(phone_number=phone_number).first()
        except Customer.DoesNotExist:
            customer = Customer.objects.create(phone_number=phone_number)
        company = CompanyInformation.objects.order_by('id').first()
        title = company.company_name if company else "Your Site"
        order =Order.objects.filter(customer=customer, complete=False).first()
        cartItems = OrderItem.objects.filter(order=order)
        total_items = cartItems.count()
            
        context = {
            'total_items': total_items,
            'order': order,
            'cartItems':cartItems,
            'company': company,
            'title' : title
        }
        return render(request, 'checkout.html', context)
    else:
        return redirect('request_access')

@csrf_exempt
def updateItem(request):
    phone_number = request.session.get('phone_number')
    if phone_number:
        try:
            customer = Customer.objects.filter(phone_number=phone_number).first()
        except Customer.DoesNotExist:
            customer = Customer.objects.create(phone_number=phone_number)

    data = json.loads(request.body)

    menuId = data['menuId']
    action = data['action']

    print('menuId:' , menuId)
    print('action:' , action)

    menu = Product.objects.filter(id=menuId).first()
    order = Order.objects.filter(customer=customer, complete=False).first()
    if not order:
        order = Order.objects.create(customer=customer, complete=False)

        orderItem= OrderItem.objects.filter(order=order, product=menu).first()
        if not orderItem:
            orderItem =OrderItem.objects.create(order=order, product=menu)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
            
            orderItem.save()
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)
                
        

            orderItem.save()

            if orderItem.quantity <= 0:
                orderItem.delete()
            

        return JsonResponse('item was added', safe= False)
    
    else:
        return redirect('request_access')


def request_access(request):
    company = CompanyInformation.objects.order_by('id').first()
    title = company.company_name if company else "Your Site"
    context ={
        'title' : title
    }
    return render(request, 'request-access.html', context)