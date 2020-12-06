from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import datetime
from django.db.models.signals import pre_save , post_save
from django.dispatch import receiver

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
    available_coins = models.IntegerField(default=0)
   
    term_condition = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True,null=True)
    update_on = models.DateTimeField(auto_now=True,null=True)
    
    otp = models.IntegerField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    referral_by = models.ForeignKey(User, null=True, blank=True ,on_delete=models.RESTRICT)
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
    user = models.ForeignKey(User, related_name='better', on_delete=models.CASCADE)
    coins = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    requested_date = models.DateTimeField(auto_now_add=True , null=True , blank=True)
    transaction_status = models.BooleanField(default=False, verbose_name="Transaction Status", blank=True, null=True, choices=TRANSACTION_STATUS)
    transaction_date = models.DateTimeField(default=timezone.now, verbose_name="Transaction On")
    game_name = models.CharField(max_length=100 , blank=True, null=True)
    
    def __str__(self):
        paid = ' paid' if self.transaction_status else ' not paid'
        return self.user.username + " requested " + str(self.coins) + paid

@receiver(post_save, sender=BetTransaction)
def my_callback(sender, instance, *args, **kwargs):
    if instance.is_paid or instance.transaction_status :
        user_info = User_info.objects.filter(user = instance.user).first()
        user_info.available_coins = user_info.available_coins - instance.coins
        user_info.save()


class GameStart(models.Model):
    game_created_by = models.ForeignKey(User , related_name="user", on_delete=models.PROTECT)
    game_slug = models.CharField(max_length=1000)
    game_status = models.CharField(max_length=100)
    game_amount = models.IntegerField(default=50)
    firebase_id = models.CharField(max_length=400 , blank=True)

class Game(models.Model):
    game_start = models.ForeignKey(GameStart, related_name="game_start" , null=True , blank=True , on_delete=models.PROTECT)
    user_one = models.ForeignKey(User ,related_name="user_one" , on_delete=models.PROTECT)
    user_two = models.ForeignKey(User ,related_name="user_two", on_delete=models.PROTECT)
    game_winner = models.ForeignKey(User , related_name="game_winner" , blank=True , null=True, on_delete=models.PROTECT)    
    betting_amount = models.IntegerField(default=0)
    room_code = models.CharField(max_length=1000)
    is_true = models.BooleanField(null=True , blank=True)
    def __str__(self):
        return self.room_code


class GameImages(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    images = models.ImageField(upload_to= 'static/gameimages')