# Generated by Django 2.2 on 2021-10-12 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0004_auto_20211012_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='approve',
            field=models.BooleanField(default=False),
        ),
    ]
