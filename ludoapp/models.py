from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import datetime
from django.db.models.signals import pre_save , post_save
from django.dispatch import receiver
from django.utils import timezone
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
    whatsapp_number = models.CharField(max_length = 30)
    available_coins = models.IntegerField(default=50)
   
    term_condition = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True,null=True)
    update_on = models.DateTimeField(auto_now=True,null=True)
    
    otp = models.IntegerField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    referral_by = models.ForeignKey(User, null=True, blank=True ,on_delete=models.RESTRICT)
    def __str__(self):
        return self.user.username


class OrderCoins(models.Model):
    user = models.ForeignKey(User  ,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    order_id = models.CharField(max_length=500 , blank=True)
    reference_id = models.CharField(max_length=500 , blank=True)
    status = models.BooleanField(default=False , blank=True)
    added_on = models.DateTimeField( default=datetime.datetime.utcnow)
    
    def __str__(self):
        return self.user.username + " ordered " + str(self.amount)


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
    requested_date = models.DateTimeField(default=timezone.now() , null=True , blank=True)
    transaction_status = models.BooleanField(default=False, verbose_name="Transaction Status", blank=True, null=True, choices=TRANSACTION_STATUS)
    transaction_date = models.DateTimeField(default=timezone.now, verbose_name="Transaction On")
    game_name = models.CharField(max_length=100 , blank=True, null=True)
    payment_option = models.CharField(max_length=100 , default="Paytm")
    phone_number = models.CharField(max_length=100 , default="User provided")
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
    user_one = models.ForeignKey(User ,related_name="user_one" , on_delete=models.PROTECT,null=True , blank=True )
    user_two = models.ForeignKey(User ,related_name="user_two", on_delete=models.PROTECT,null=True , blank=True)
    game_winner = models.ForeignKey(User , related_name="game_winner" , blank=True , null=True, on_delete=models.PROTECT)    
    
    result_user_one = models.CharField(max_length=100 , blank=True , null=True)
    result_user_two = models.CharField(max_length=100 , blank=True , null=True)
    
    flagged_as_disputed = models.BooleanField(default=False)
    
    betting_amount = models.IntegerField(default=0)
    room_code = models.CharField(max_length=1000, null=True , blank=True)
    is_true = models.BooleanField(null=True , blank=True)
    
    def __str__(self):
        return self.room_code
    
class DisputedGame(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    date_of_disputed = models.DateTimeField(auto_now_add=True)


def addMoney(user_id , amount):
    user = User.objects.get(id=user_id)
    user_info = User_info.objects.filter(user=user).first()
    amount_in_percentage = .95 * (amount / 2) 
    user_info.available_coins += amount_in_percentage
    user_info.save()
    
def deductMoney(user_id , amount):
    user = User.objects.get(id=user_id)
    user_info = User_info.objects.filter(user=user).first()
    user_info.available_coins -= (amount / 2)
    user_info.save()
    
    
class GameWinnerLoose(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE , blank=True , null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    win_or_lost = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)    

@receiver(post_save, sender=GameWinnerLoose)   
def win_loose_handler(sender, instance, *args, **kwargs):
    if instance.win_or_lost:
        addMoney(instance.user.id , instance.amount)
    else:
        deductMoney(instance.user.id ,instance.amount)
        
         
    


@receiver(post_save, sender=Game)
def game_handler(sender, instance, *args, **kwargs):
    if instance.result_user_one and instance.result_user_two:
        win_id = None
        lost_id = None
        if instance.result_user_one == 'WON' and instance.result_user_two == 'LOST':
            win_id = instance.user_one
            lost_id = instance.user_two
            instance.game_winner = instance.user_one
            addMoney(instance.user_one.id ,instance.betting_amount)
            deductMoney(instance.user_two.id ,instance.betting_amount)
        elif instance.result_user_one == 'LOST' and instance.result_user_two == 'WON':
            win_id = instance.user_two
            lost_id = instance.user_one
            instance.game_winner = instance.user_two
            addMoney(instance.user_two.id , instance.betting_amount)
            deductMoney(instance.user_one.id ,instance.betting_amount)
        elif (instance.result_user_one == 'WON' and instance.result_user_two == 'WON') or (instance.result_user_one == 'LOST' and instance.result_user_two == 'LOST') :
            disputed_game = DisputedGame(game = instance)
            disputed_game.save()
            
        if win_id is not None and lost_id is not None:
            game_obj_one = GameWinnerLoose(game = instance ,user=win_id , win_or_lost=True, amount= instance.betting_amount)
            game_obj_two = GameWinnerLoose(game = instance ,user=lost_id , amount= instance.betting_amount)
            game_obj_one.save()
            game_obj_two.save()
            
            
    

class GameImages(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    images = models.ImageField(upload_to= 'static/gameimages')
    



class Penalty(models.Model):
    user = models.ForeignKey(User , on_delete=models.PROTECT)
    amount =models.IntegerField(default=0)
    reason_of_penalty = models.CharField(max_length=400)
    added_on = models.DateTimeField( default=datetime.datetime.utcnow)
    
    def save(self, *args, **kwargs):
        user = User_info.objects.get(user = self.user)
        user.available_coins -= self.amount
        user.save()
        super(Penalty,self).save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username + ' ' + self.reason_of_penalty