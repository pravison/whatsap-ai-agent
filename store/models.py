from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont 
import json
from tinymce.models import HTMLField

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    product_photo = models.ImageField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    description = HTMLField()
    offer = HTMLField(blank=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, help_text='qr code is aumatically generated just leave it as it is')

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.product_photo.url
        except:
            url = ''
        return url
    
    def generate_qr_code(self, domain_url):
        # generate product infor as a dictionary
        product_info ={
            'name': self.name,
            'price': str(self.price),
        }
        # convert product infor into json string
        product_data=json.dumps(product_info)
        """
        generate qr code with a dynamic product url
        """
        qr = qrcode.QRCode(version=1, box_size=10, border=5)

        # construct product url that is dynamic
        product_url = f"https://{domain_url}/product/{ self.id }/"

        qr.add_data(product_url)
        # qr.add_data(product_data)
        qr.make(fit=True)

        # create qrcode image
        img = qr.make_image(fill='black', back_color='white')

        # create new blank image large enough to hold both qrcode and text
        qr_width, qr_height = img.size
        total_height = qr_height + 30  #extra space for text
        new_img = Image.new('RGB', (qr_width, total_height), 'white')
        # paste qr_code image to new blank image
        new_img.paste(img, (0,0))
        # initialize to draw foe new image
        draw = ImageDraw.Draw(new_img)
        # set up the font
        try:
            font = ImageFont.truetype("ariel.ttf", 60)
        except IOError:
            font = ImageFont.load_default()

        # define text
        text = "scan to view price"
        text_bbox = draw.textbbox((0,0), text, font=font)
        # calculate text height and width from bounding box
        text_width =  text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_position = ((qr_width - text_width)//2, qr_height + 5)
        # add text to the new_img
        draw.text(text_position, text, fill='black', font=font)
        # saving the final image
        buffer = BytesIO()
        new_img.save(buffer, 'PNG')
        self.qr_code.save(f'{self.name}_qr.png', File(buffer), save=False)
        self.save()

    def save(self, *args, **kwargs):
        # extract tenat domain from request or tenant context 
        domain_url = kwargs.pop('domain_url', None)
        if not self.id:
            super().save(*args, **kwargs)
        if domain_url and not self.qr_code:
            self.generate_qr_code(domain_url)
        super().save(*args, **kwargs)

