# Generated by Django 3.1.3 on 2020-12-13 07:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ludoapp', '0015_auto_20201213_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bettransaction',
            name='requested_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 13, 7, 59, 42, 667242, tzinfo=utc), null=True),
        ),
    ]