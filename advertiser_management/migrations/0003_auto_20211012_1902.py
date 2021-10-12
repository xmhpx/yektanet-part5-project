# Generated by Django 2.2 on 2021-10-12 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0002_auto_20211012_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='clicks',
        ),
        migrations.RemoveField(
            model_name='ad',
            name='views',
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('user_ip', models.GenericIPAddressField()),
                ('ad_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertiser_management.Ad')),
            ],
        ),
        migrations.CreateModel(
            name='Click',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('user_ip', models.GenericIPAddressField()),
                ('ad_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertiser_management.Ad')),
            ],
        ),
    ]