from django.conf import settings 
from datetime import  datetime, timedelta
from django.utils import timezone
from customers.models import Conversation, Customer
import requests
import openai
from ai.models import TaskPipeline, Escalation, AI_Agent, SalesFunnelStageInstruction
from accounts.models import CompanyInformation


# Set up OpenAI API key 
openai.api_key =settings.OPENAI_API_KEY

def receiveCall(audio):
    pass

def callClient(audio):
    pass


#######################################################################################################################################################
# sending message to whatsap
########################################################################################################################################################


whatsapp_url =settings.WHATSAPP_URL
whatsapp_token =settings.WHATSAPP_TOKEN
def sendWhatsappMessage(fromId, message):
    headers = {"Authorization" : whatsapp_token}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type" : "individual",
        "to": fromId,
        "type":"text",
        "text":{"body": message}
        }
    requests.post(whatsapp_url, headers=headers, json=payload)
    return True


#######################################################################################################################################################
# cutomer support agent
########################################################################################################################################################
    

# ductionary containing follow up instruction , depending on sales funnel stages 
FOLLOW_UP_INSTRUCTIONS = {
    'awareness': """
            Goal: Introduce your product/service.
            SOP:

            Research the target market and audience.
            Call, SMS, or WhatsApp the customer to introduce your product and its value.
            Keep the message short, highlighting a key problem and your solution.
            End with a clear CTA (e.g., schedule a call, visit website, or download resources).
            Log responses to track who shows interest for follow-up.
        """,
    'interest': """
            Goal: Engage prospects who show interest.
            SOP:
            Segment leads based on initial responses or missed calls.
            Call or WhatsApp them within 24-48 hours to follow up on their interest.
            Send personalized content via WhatsApp or SMS (e.g., case studies, testimonials).
            Offer to answer any questions or schedule a live demo.
            Track their engagement by noting call responses or content read in WhatsApp.
        """,
    'decision': """
            Goal: Help prospects evaluate and choose your solution.
            SOP:

            Call them to provide a tailored offer or clarify product features.
            Use WhatsApp or SMS to send product comparisons or limited-time promotions.
            Offer to schedule a one-on-one demo or consultation.
            Handle objections by discussing concerns over the call or sending clarifying information via SMS.
            Set up a follow-up call at a convenient time to keep the conversation going.
        """,
    'purchase': """
            Goal: Convert leads into paying customers.
            SOP:

            Call to guide them through the purchase process and confirm details.
            Use WhatsApp or SMS to provide payment links or instructions.
            Send a confirmation message once the purchase is completed.
            Offer immediate support through WhatsApp or phone to ensure a smooth transition.
            Request a review or referral via WhatsApp after successful onboarding.
        """,
    'active': """
            Goal: Retain and upsell existing customers.
            SOP:

            Call regularly to check on their satisfaction and ensure they’re utilizing the product fully.
            Send updates, new feature announcements, or upsell options through WhatsApp or SMS.
            Offer personalized promotions or loyalty discounts via phone or message.
            Provide a direct support line for them to contact you easily via phone or WhatsApp.
            Gather feedback through phone calls to strengthen the customer relationship.
        """,  
    'dormant': """
            Goal: Re-engage inactive customers.
            SOP:

            Identify dormant customers through CRM.
            Call to check in and remind them of your services.
            Send personalized re-engagement offers via WhatsApp or SMS.
            Highlight key benefits or provide a special offer to encourage action.
            Log responses from calls or messages and adjust future re-engagement strategies based on their feedback.
        """,  
}


# Define keywords or phrases that indicate the customer is busy
BUSY_KEYWORDS = [
    "busy", "call later", "can't talk now", "react out later", "later", "another time", "not now", "contact me next month"
]

def is_customer_busy(customer_message):
    """
    Check if the customer's message indicates they are busy.

    Parameters:
    - customer_message (str): The message from the customer.

    Returns:
    - bool: True if the customer is busy, False otherwise.
    """
    message = customer_message.lower()
    return any(keyword in  message for keyword in BUSY_KEYWORDS)


def get_past_conversations(customer):
    """
    Retrieve past conversation history for the given customer.

    Parameters:
    - customer (Customer object): The customer whose conversation history we want to retrieve.

    Returns:
    - str: A string representing the concatenated past conversation history.
    - bool: A flag indicating whether this is the customer's first interaction.
    """
    chats = Conversation.objects.filter(customer=customer).order_by('timestamp')
    
    if not chats.exists():
        # No previous chats, so it's the first interaction
        return "", True
    
    conversation_history = ""
    
    for chat in chats:
        if chat.sender =='customer':
            conversation_history += f"Customer: {chat.message}\n"
        else:
            conversation_history += f"AI: {chat.message}\n"
    
    return conversation_history, False


def save_conversation(customer, customer_message, ai_response):
    """
    Save the customer's message and the AI response to the Chat model.

    Parameters:
    - customer (Customer object): The customer associated with the chat.
    - customer_message (str): The message from the customer.
    - ai_response (str): The response from the AI.

    Returns:
    - None2
    """
    # Save customer's message
    Conversation.objects.create(
        customer=customer,
        message=customer_message,
        sender='customer'
    )

    # Save AI's response
    Conversation.objects.create(
        customer=customer,
        message=ai_response,
        sender='AI'
    )



def escalation_needed(customer, customer_message, ai_response):
    """
    Check if the AI response indicates the need for escalation.

    Parameters:
    - ai_response (str): The response generated by the AI.

    Returns:
    - bool: True if escalation is needed, False otherwise.
    """
    escalation_keywords = ['escalate', 'help from human', 'support agent', 'can’t assist', 'need human']
    
    # Check if any escalation keyword is in the AI response
    if any(keyword in customer_message.lower() for keyword in escalation_keywords):
        escalate, created = Escalation.objects.get_or_create(customer=customer)
    
        # Assuming you have fields follow_up_date and follow_up_time in TaskPipeline
        escalate.reasons = customer_message
        escalate.save()

    elif any(keyword in ai_response.lower() for keyword in escalation_keywords):
        escalate, created = Escalation.objects.get_or_create(customer=customer)
    
        # Assuming you have fields follow_up_date and follow_up_time in TaskPipeline
        escalate.reasons = customer_message
        escalate.save()
    return ''


def update_funnel_stage(customer, customer_message):
    """
    Update the customer's sales funnel stage based on their message.

    Parameters:
    - customer (Customer object): The customer record from the database.
    - customer_message (str): The latest message from the customer.

    Returns:
    - new_funnel_stage (str): Updated funnel stage for the customer.
    """
    if any(keyword in customer_message.lower() for keyword in ["interested","intrested", "details", "more information"]):
        new_funnel_stage = "interest"
    elif any(keyword in customer_message.lower() for keyword in ["ready", "purchase", "buy"]):
        new_funnel_stage = "decision"
        # update this other funnels stages later 
    # elif any(keyword in customer_message.lower() for keyword in ["ready", "purchase", "buy"]):
    #     new_funnel_stage = "purcahse"
    # elif any(keyword in customer_message.lower() for keyword in ["ready", "purchase", "buy"]):
    #     new_funnel_stage = "active"
    # elif any(keyword in customer_message.lower() for keyword in ["ready", "purchase", "buy"]):
    #     new_funnel_stage = "dormant"
    else:
        new_funnel_stage = customer.funnel_stage 

    # Update the funnel stage in the database (pseudo-code)
    customer.funnel_stage = new_funnel_stage
    customer.save()

    return new_funnel_stage



def handle_customer_query(customer_message, customer):
    """
    Handles a customer query, introducing yourself on the first interaction while responding to the query.

    Parameters:
    - customer_message (str): The new message from the customer.
    - customer_data (dict): Information about the customer, including name, company, and funnel stage.

    Returns:
    - AI response, new funnel stage, escalation flag
    """
    company, created = CompanyInformation.objects.get_or_create(id=1, defaults={"company_name": "Your Site"})
    agent, created = AI_Agent.objects.get_or_create(id=1, defaults={"agent_name": "sales agent"})
    # Get the past conversation history and check if it's the first interaction
    past_history, is_first_interaction = get_past_conversations(customer)

    # Prepare the introduction message if it's the first interaction
    if is_first_interaction:
        introduction_message = f"Hello! I’m {agent.agent_name if agent and hasattr(agent, 'agent_name') else 'SalesGenie'}, your AI assistant working with {company.company_name if company and hasattr(company, 'acompany_name') else 'Salesflow Pro'}. "
    else:
        introduction_message = ""

    
    instructions = SalesFunnelStageInstruction.objects.filter(funnel_stage=customer.funnel_stage).first()
    if instructions:
       follow_up_instructions= SalesFunnelStageInstruction.objects.filter(funnel_stage=customer.funnel_stage).first()
    else:
        follow_up_instructions= FOLLOW_UP_INSTRUCTIONS.get(customer.funnel_stage, """
            Goal: Engage prospects who show interest.
            SOP:
            Segment leads based on initial responses or missed calls.
            Call or WhatsApp them within 24-48 hours to follow up on their interest.
            Send personalized content via WhatsApp or SMS (e.g., case studies, testimonials).
            Offer to answer any questions or schedule a live demo.
            Track their engagement by noting call responses or content read in WhatsApp.
        """)
    # Prepare the full prompt including the introduction if necessary
    prompt = f"""
    {introduction_message}
    
    You are an AI sales assistant named {agent.agent_name if agent and hasattr(agent, 'agent_name') else 'SalesGenie'}, working for {company.company_name}.
    The customer is in the {customer.funnel_stage} stage of the sales funnel, and their name is {customer.name}.

    The product/service you're promoting is {company.products_summary}.

    The company description  is {company.company_description}.

    Below is the past conversation history: {past_history}

    Guidelines for your response:
    - Use a friendly, engaging tone.
    {follow_up_instructions}

    Now, the customer said: "{customer_message}"

    Respond to the customer, taking into account their query and their position in the sales funnel.
    If it’s the first interaction, introduce yourself, and then respond appropriately to the customer's message. 
    If escalation is needed, just reply you will be escalated to hunan agent to be assisted.
    """

    # Call OpenAI API to generate a response based on the dynamic prompt
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful AI sales assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Parse the response
    ai_response = response['choices'][0]['message']['content']

    save_conversation(customer, customer_message, ai_response)

    # handle escalations
    escalation_needed(customer, customer_message, ai_response)

    # handle Update funnel stage based on customer message (e.g., based on keywords like "interested")
    update_funnel_stage(customer, customer_message)

    
    print(ai_response)
    return ai_response  

import dateparser
import re

def extract_time(message):
    """
    Extracts time from the message using regex to handle formats like '3pm', '15:00', etc.
    """
    time_pattern = r'(\d{1,2}(?::\d{2})?\s?(?:am|pm)?)'
    match = re.search(time_pattern, message, re.IGNORECASE)
    if match:
        return match.group(0)
    return None

def extract_follow_up_datetime(customer_message):
    """
    Extracts a follow-up date and time from the customer's message.
    
    Returns a datetime object or None if parsing fails.
    """
    customer_message = customer_message.lower()

    # Default follow-up date is today
    follow_up_date = datetime.now()

    # Check for keywords like 'tomorrow' and adjust the date
    if "tomorrow" in customer_message:
        follow_up_date = follow_up_date + timedelta(days=1)

    # You can add more logic for other keywords like "next week", etc.

    # Extract the time from the message
    time_str = extract_time(customer_message)

    if time_str:
        # Parse the time (e.g., '3pm' -> '15:00')
        follow_up_time = datetime.strptime(time_str, '%I%p' if 'pm' in time_str or 'am' in time_str else '%H:%M').time()
        follow_up_datetime = datetime.combine(follow_up_date, follow_up_time)
    else:
        # If no time is found, return the default date (just the day, no specific time)
        follow_up_datetime = follow_up_date

    print(f"Extracted datetime: {follow_up_datetime}")
    return follow_up_datetime


def update_follow_up_in_task_pipeline(task_pipeline, follow_up_datetime):
    """
    Updates the TaskPipeline for the customer with the provided follow-up time and date.

    Parameters:
    - customer: The customer object.
    - follow_up_date: The date for follow-up.
    - follow_up_time: The time for follow-up.

    Returns:
    - None
    """
    # Assuming you have fields follow_up_date and follow_up_time in TaskPipeline
    task_pipeline.follow_up_date = follow_up_datetime.date()
    task_pipeline.follow_up_time = follow_up_datetime.time()
    
    task_pipeline.save()


def handle_customer_query_with_follow_up(customer_message, fromId):
    """
    Handles a customer query, detecting if the customer is busy and handling follow-up scheduling.

    Parameters:
    - customer_message (str): The new message from the customer.
    - customer_data (dict): Information about the customer, including name and funnel stage.

    Returns:
    - AI response, updated funnel stage, escalation flag
    """
    #getting customer 
    customer, created = Customer.objects.get_or_create(
            phone_number=fromId
        )
    #adding this to last time talked with the customer
    customer.last_talked = timezone.now().date()
    customer.save()
    #getting the previous chat 
    # previous_chat = Conversation.objects.filter(customer=customer ).order_by('-timestamp').first()
    # last_chat = previous_chat if previous_chat is not None else ""
    # Check if customer indicates they are busy
    if is_customer_busy(customer_message):
        # AI response asking for a convenient time and date
        ai_response = f"Thank you for letting me know! I appreciate your time. Could you please let me know a more convenient time and date for us to follow up?"

        # Save this interaction in the TaskPipeline for later follow-up
        task_pipeline, created = TaskPipeline.objects.get_or_create(customer=customer)
        # task_pipeline.follow_up_scheduled = True
        task_pipeline.save()

        #  the above function was trying to extract time and date and be able to add it to task pipeline but it does not work 

        follow_up_datetime = extract_follow_up_datetime(customer_message)

        if follow_up_datetime:
            ai_response = f"Thank you! I have scheduled a follow-up for {follow_up_datetime.strftime('%A, %B %d at %I:%M %p')}."
            update_follow_up_in_task_pipeline(task_pipeline, follow_up_datetime)
        else:
            ai_response = "Sorry, I couldn't understand the follow-up time. Could you please provide a specific time and date?"

        return ai_response
    #     # cheking if previous messaage had busy in it 
    # elif is_customer_busy(last_chat):
    #     follow_up_datetime = extract_follow_up_datetime(customer_message)

    #     if follow_up_datetime:
    #         ai_response = f"Thank you! I have scheduled a follow-up for {follow_up_datetime.strftime('%A, %B %d at %I:%M %p')}."
    #         update_follow_up_in_task_pipeline(customer, follow_up_datetime)
    #     else:
    #         ai_response = "Sorry, I couldn't understand the follow-up time. Could you please provide a specific time and date?"


    #     return ai_response
    else:
        # Handle the normal flow (responding to queries, etc.)
        return handle_customer_query(customer_message, customer)


#bring it all together 
#lets define the function thart talk to webhook
def handleWhatsappCall(fromId, customer_message):
    message = handle_customer_query_with_follow_up(customer_message, fromId)
    sendWhatsappMessage(fromId, message)
    

#######################################################################################################################################################
# leads warmup agent
########################################################################################################################################################

# function that checks the last time customer was called and the add customer to TaskPipeline

# Define the minimum follow-up days for each funnel stage
FOLLOW_UP_DAYS = {
    'awareness': 5,
    'interest': 3,
    'decision': 2,
    'purchase': 1,
    'active': 7,   # Assuming 1-2 weeks; using the minimum of 7 days
    'dormant': 30  # Assuming 30-60 days; using the minimum of 30 days
}

def add_customers_to_pipeline():
    # Get the current date
    current_date = timezone.now().date()
    
    # Get all customers who haven't been talked to recently based on their funnel stage
    customers_to_follow_up = Customer.objects.all()

    # Iterate over each customer and determine if they need a follow-up
    for customer in customers_to_follow_up:
        # Get the follow-up threshold based on the customer's funnel stage
        follow_up_days = FOLLOW_UP_DAYS.get(customer.funnel_stage, 3)  # Default to 3 days if no stage matches
        
        # Check if the last talked date exceeds the threshold
        if customer.last_talked < current_date - timedelta(days=follow_up_days):
            # Check if the customer is already in the pipeline and the task is not done
            existing_task = TaskPipeline.objects.filter(customer=customer, done=False).exists()
            
            if not existing_task:  # Only add if no active task exists
                TaskPipeline.objects.create(
                    customer=customer,
                    follow_up_date=current_date + timedelta(days=1),  # Set follow-up date for the next day
                    follow_up_time=None,  # You can set a default time here if needed
                )
                print(f"Added {customer.phone_number} to TaskPipeline")

# leads warmup agent
def follow_up_tasks_today():
    """
    This function checks all tasks in TaskPipeline that have a follow-up date of today
    and initiates a follow-up process for each of them.
    
    Returns:
    - A list of follow-up results for each customer.
    """
    company, created = CompanyInformation.objects.get_or_create(id=1, defaults={"company_name": "Your Site"})
    agent, created = AI_Agent.objects.get_or_create(id=1, defaults={"agent_name": "sales agent"})
    # Get the current date
    current_date = timezone.now().date()

    # Get all tasks with a follow-up date of today
    tasks_to_follow_up = TaskPipeline.objects.filter(follow_up_date=current_date, done=False)

    # Iterate over each task and follow up with the respective customer
    for task in tasks_to_follow_up:
        customer = task.customer

        # Get the past conversation history and check if it's the first interaction
        past_history, is_first_interaction = get_past_conversations(customer)

        # Prepare the introduction message if it's the first interaction
        if is_first_interaction:
            introduction_message = f"Hello! I’m {agent.agent_name if agent and hasattr(agent, 'agent_name') else 'SalesGenie'}, your AI assistant working with {company.company_name if company and hasattr(company, 'acompany_name') else 'Salesflow Pro'}. "
        else:
            introduction_message = ""

        # getting guidin sops depending on customer sales funnel stage
        instructions = SalesFunnelStageInstruction.objects.filter(funnel_stage=customer.funnel_stage).first()
        if instructions:
            follow_up_instructions= SalesFunnelStageInstruction.objects.filter(funnel_stage=customer.funnel_stage).first()
        else:
            follow_up_instructions= FOLLOW_UP_INSTRUCTIONS.get(customer.funnel_stage, """
                Goal: Engage prospects who show interest.
                SOP:
                Segment leads based on initial responses or missed calls.
                Call or WhatsApp them within 24-48 hours to follow up on their interest.
                Send personalized content via WhatsApp or SMS (e.g., case studies, testimonials).
                Offer to answer any questions or schedule a live demo.
                Track their engagement by noting call responses or content read in WhatsApp.
            """)
        
        # Prepare the full prompt including the introduction if necessary
        prompt = f"""
        {introduction_message}
        
        You are an AI sales assistant named {agent.agent_name if agent and hasattr(agent, 'agent_name') else 'SalesGenie'}, working for {company.company_name}.
        Your role is to guide customers through the sales funnel by providing helpful, friendly, and timely responses that nutures customers untill they are ready to purchase.
        
        The customer is currently in the {customer.funnel_stage} stage of the sales funnel, and their name is {customer.name if customer and hasattr(customer, 'name') else 'Customer'}.
        
        The product/service you're promoting is {company.products_summary}.

        The company description  is {company.company_description}.
        
        Below is the past conversation history with the customer:
        {past_history}

        Follow the specific instructions below to shape your response:

        {follow_up_instructions}

        Guidelines for your response:
        - Use a friendly, engaging tone.
        {follow_up_instructions}

        Respond thoughtfully, addressing the customer's needs based on their position in the funnel, while maintaining a friendly and helpful tone. If it’s the first interaction, introduce yourself and be informative. If escalation is required, ensure the customer knows they will be connected with a human agent.
        """

        # Call OpenAI API to generate a response based on the dynamic prompt
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI sales assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Parse the response
        ai_response = response['choices'][0]['message']['content']

        # sending the follow up message 
        fromId = customer.phone_number
        message = ai_response
        sendWhatsappMessage(fromId, message)
        
        # Save AI's folow up message 
        Conversation.objects.create(
            customer=customer,
            message=ai_response,
            sender='AI'
        )
        # Mark the task as done (or update it as necessary)
        task.done = True
        task.save()

        # Optionally, print out for testing purposes
        print(f"Followed up with {customer.name} ({customer.phone_number})")

    return True

