# Generated by Django 3.1.3 on 2020-12-12 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ludoapp', '0013_gamewinnerloose_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='bettransaction',
            name='payment_option',
            field=models.CharField(default='Paytm', max_length=100),
        ),
        migrations.AddField(
            model_name='bettransaction',
            name='phone_number',
            field=models.CharField(default='User provided', max_length=100),
        ),
    ]
