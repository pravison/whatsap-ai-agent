from django.db import models
from store.models import Product
# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    whatsapp_profile = models.CharField(max_length=200, blank=True, null=True)
    funnel_stage = models.CharField(max_length=50, default='awareness', choices=(('awareness', 'awareness'), ('interest', 'interest'),('decision', 'decision'), ('purchase', 'purchase'), ('active', 'active'), ('dormant', 'dormant'))) # active for active customer and dormant for dormant customer
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField( blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add = True)
    last_talked = models.DateField(blank=True, null=True)


    def __str__(self):
        return f" {self. whatsapp_profile} phone number - {self.phone_number}"
    
class Conversation(models.Model):
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True, related_name='conversations')
    sender = models.CharField(max_length=50, choices=(('customer', 'customer'), ('AI', 'AI')))
    message = models.TextField()
    read = models.BooleanField(default=False)
    date_added = models.DateField(auto_now_add = True, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"

class CustomerHistory(models.Model):
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    CUSTOMER_HISTORY_CHOICES={
        'view': 'view',
        'add to cart' : 'add to cart',
        'purchased' : 'purchased'
    } 
    history_status = models.CharField(max_length=100, default='view', choices=CUSTOMER_HISTORY_CHOICES)
    date = models.DateField(auto_now_add=True)
    time= models.TimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.date} @ {self.time}'




class Order(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.SET_NULL , null= True, blank=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, blank=True, null=True)
    total_order_items = models.IntegerField(default=0)
    total_order_total = models.IntegerField(default=0)

    def __str__(self):
        return f' {str(self.id)}  {self.date_orderd}'
    
    @property
    def get_cart_total(self):
        orderitems =self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems =self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        try:
            return self.product.name
        except:
            return f'no product name'
    
    @property
    def get_total(self):
        try:
            total = self.product.price * self.quantity
        except:
            total= self.product.price

        return total
