# Generated by Django 4.1.7 on 2023-03-10 23:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_alter_memos_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='memos',
            name='subusers',
            field=models.ManyToManyField(blank=True, related_name='submemo', to=settings.AUTH_USER_MODEL),
        ),
    ]
