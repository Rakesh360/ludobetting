# Generated by Django 3.1.3 on 2020-12-12 18:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ludoapp', '0014_auto_20201213_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bettransaction',
            name='requested_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 12, 18, 51, 8, 768424, tzinfo=utc), null=True),
        ),
    ]
