# Generated by Django 4.1.7 on 2023-02-22 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0003_rename_labels_keywords_rename_label_keywords_keyword_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memos',
            name='keywords',
            field=models.ManyToManyField(blank=True, related_name='memos', to='apps.keywords'),
        ),
    ]
