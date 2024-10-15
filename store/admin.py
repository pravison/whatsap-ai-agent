from django.contrib import admin
from .models import Product
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from whatsapp.settings import BASE_DIR
import environ
import os

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
VERCEL_BLOB_URL = env('VERCEL_BLOB_URL')
# Register your models here.
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'qr_code', 'product_photo')
    search_fields = ('name',)
    
    def save_model(self, request, obj, form, change):
        # Handle product photo upload to Vercel Blob
        if 'product_photo' in request.FILES:
            uploaded_file = request.FILES['product_photo']
            
            # Save the product photo locally (optional step if you need local storage as well)
            local_file_path = os.path.join('media', uploaded_file.name)

            # Save the uploaded product photo locally
            with default_storage.open(local_file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Construct the public URL for the product photo in Vercel Blob
            photo_url = os.path.join(VERCEL_BLOB_URL , uploaded_file.name)  # Construct the public URL

            # Update the object with the product photo's URL
            obj.product_photo = photo_url
        
        # Handle QR code generation and saving
        tenant_domain = request.get_host()  # Get the tenant's domain for QR code generation
        obj.save(domain_url=tenant_domain)

        super().save_model(request, obj, form, change)

admin.site.register(Product, ProductAdmin)

        

admin.site.register(Product, ProductAdmin)

