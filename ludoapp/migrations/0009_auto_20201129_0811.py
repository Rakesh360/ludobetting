# Generated by Django 3.1.3 on 2020-11-29 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ludoapp', '0008_auto_20201129_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bettransaction',
            name='transaction_status',
            field=models.BooleanField(blank=True, choices=[(True, 'success'), (False, 'failed')], default=False, null=True, verbose_name='Transaction Status'),
        ),
    ]
