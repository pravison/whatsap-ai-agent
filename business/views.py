from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .functions import handleWhatsappCall, follow_up_tasks_today, add_customers_to_pipeline, save_conversation
from customers.models import Customer, Conversation
from accounts.models import CompanyInformation, Whatsapp
from ai.models import TaskPipeline, Escalation
import json
from django.utils import timezone


current_date = timezone.now().date()
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(10)

processed_message_ids = set()

@login_required
def index(request):
    chats= Conversation.objects.filter(date_added=current_date)
    total_chats = chats.count()
    tasks= TaskPipeline.objects.filter(follow_up_date=current_date, done=True)
    total_tasks = tasks.count()
    escalations = Escalation.objects.filter(date=current_date)
    total_escalations = escalations.count()
    company = CompanyInformation.objects.order_by('id').first()
    title = company.company_name if company else "Your Site"
    return render(request, 'index.html', {'title' : title, 'total_chats': total_chats, 'total_tasks': total_tasks, 'total_escalations': total_escalations })

def terms(request):
    company = CompanyInformation.objects.order_by('id').first()
    title = company.company_name if company else "Your Site"
    context = {
       
    }
    return render(request, 'terms.html', context)
def privacy(request):
    company = CompanyInformation.objects.order_by('id').first()
    title = company.company_name if company else "Your Site"
    context = {
       
    }
    return render(request, 'policy.html', context)
        
@csrf_exempt
def whatsappWebhook(request):
    whatsapp = Whatsapp.objects.filter(id=1).first()
    if request.method == "GET":
        VERIFY_TOKEN = whatsapp.whatsapp_verify_token
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse('error', status=403)
        
    if request.method == 'POST':
        data = json.loads(request.body)
        if 'object' in data and data['object'] == 'whatsapp_business_account':
            try:
                for entry in data.get('entry', []):
                    changes = entry.get('changes', [])
                    if changes:
                        value = changes[0].get('value', {})
                        metadata = value.get('metadata', {})
                        phoneId = metadata.get('phone_number_id')
                        contacts = value.get('contacts', [])
                        if contacts:
                            profileName = contacts[0].get('profile', {}).get('name')
                            # whatsAppId = contacts[0].get('wa_id')
                        messages = value.get('messages', [])
                        if messages:
                            fromId = messages[0].get('from')
                            text = messages[0].get('text', {}).get('body')
                            message_id = messages[0].get('id')


                            # Check if customer with the phone number exists
                            request.session['phone_number'] = 'fromId'
                            customer, created = Customer.objects.get_or_create(
                                phone_number=fromId,
                                defaults={
                                    'whatsapp_profile': profileName,
                                }
                            )
                            sender = 'customer'
                            message = text
                            save_conversation(customer, message, sender )
                            # Process the message only if it hasn't been processed before
                            if message_id not in processed_message_ids:
                                customer_message = text
                                handleWhatsappCall(fromId, customer_message)
                                processed_message_ids.add(message_id)
                                break
                            break

            except Exception as e:
                print(f"Error processing webhook data: {e}")
                return HttpResponse('error', status=500)
        else:
            return HttpResponse('error', status=400)

        return HttpResponse('success', status=200)
    
@login_required
def leadsWarmupPage(request):
    # Get all tasks with a follow-up date of today
    tasks = TaskPipeline.objects.filter(follow_up_date=current_date, done=False)
    company = CompanyInformation.objects.filter(id=1).first()
    title = company.company_name if company else "Your Site"
    context = {
       'title' : title,
       'tasks' : tasks
    }
    return render(request, 'leads_warmup.html', context)

@login_required
def addCustomersForFollowUp(request):
    add_customers_to_pipeline()
    return redirect('leads_warmup_page')

@login_required
def customersForFollowUp(request):
    follow_up_tasks_today()
    return redirect('leads_warmup_page')