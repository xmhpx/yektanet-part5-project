# Generated by Django 2.2 on 2021-10-24 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0005_ad_approve'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starttime', models.DateTimeField()),
                ('endtime', models.DateTimeField()),
                ('click_cnt', models.IntegerField()),
                ('view_cnt', models.IntegerField()),
            ],
        ),
    ]
