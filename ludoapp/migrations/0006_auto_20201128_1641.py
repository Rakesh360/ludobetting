# Generated by Django 3.1.3 on 2020-11-28 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ludoapp', '0005_auto_20201128_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bettransaction',
            name='game_name',
            field=models.CharField(choices=[('ludo', 'Ludo'), ('snake_n_ladders', "Snake 'n Ladders")], max_length=50),
        ),
    ]
