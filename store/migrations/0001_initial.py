# Generated by Django 5.0.7 on 2024-10-12 08:06

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', tinymce.models.HTMLField()),
                ('offer', tinymce.models.HTMLField(blank=True)),
                ('qr_code', models.ImageField(blank=True, upload_to='qr_codes')),
            ],
        ),
    ]
