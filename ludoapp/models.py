from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import datetime

GAMES_AVAILABLE = (
    ('ludo', 'Ludo'),
    ('snake_n_ladders', "Snake 'n Ladders"),
)

TRANSACTION_STATUS = (
    (True, 'success'),
    (False, 'failed')
)

class User_info(models.Model):
    user = models.OneToOneField(User, related_name='agreement', on_delete=models.CASCADE)
    whatsapp_number = models.IntegerField()
    available_coins = models.IntegerField(blank=True, null=True)
   
    term_condition = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True,null=True)
    update_on = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.user.username



class Contact_Us(models.Model):
    name = models.CharField(max_length=250)
    contact_number = models.IntegerField(blank=True,unique=True)
    subject = models.CharField(max_length=250)
    message = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Contact Us"





class Add_coins(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    transection_id = models.CharField(max_length=250)
    amount = models.FloatField()
    added_on =models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return self.transection_id



class Sell_coins(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    paytm_number = models.CharField(max_length=20)
    amount = models.FloatField()
    status = models.BooleanField(default=False)
    processed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cust_id.username


class BetTransaction(models.Model):
    user = models.OneToOneField(User, related_name='better', on_delete=models.CASCADE)
    coins = models.IntegerField()
    game_name = models.CharField(max_length=50, choices=GAMES_AVAILABLE)
    transaction_status = models.BooleanField(default=False, verbose_name="Transaction Status", blank=True, null=True, choices=TRANSACTION_STATUS)
    transaction_date = models.DateTimeField(default=timezone.now, verbose_name="Transaction On")
