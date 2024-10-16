# Generated by Django 5.0.7 on 2024-09-15 16:15

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0002_escalation_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesFunnelStageInstruction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('funnel_stage', models.CharField(choices=[('awareness', 'awareness'), ('interest', 'interest'), ('decision', 'decision'), ('purchase', 'purchase'), ('active', 'active'), ('dormant', 'dormant')], max_length=50)),
                ('instructions', tinymce.models.HTMLField(help_text="write you sales SOP'S depending on the funnel stage you choose. provide instructions to all the above stages")),
            ],
        ),
    ]
