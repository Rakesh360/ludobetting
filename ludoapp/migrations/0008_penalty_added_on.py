# Generated by Django 3.1.3 on 2020-12-09 07:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ludoapp', '0007_ordercoins_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='penalty',
            name='added_on',
            field=models.DateTimeField(default=datetime.datetime.utcnow),
        ),
    ]