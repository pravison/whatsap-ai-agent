# Generated by Django 5.0.7 on 2024-09-15 16:14

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0003_salesfunnelstageinstruction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesfunnelstageinstruction',
            name='instructions',
            field=tinymce.models.HTMLField(help_text="write you sales SOP'S depending on the funnel stage you choose. provide instructions to all the above stages", max_length=500),
        ),
    ]
