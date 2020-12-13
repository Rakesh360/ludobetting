from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from ludoapp.models import (
    User_info, 
    Add_coins, 
    Sell_coins, 
    Contact_Us, 
    BetTransaction,
    GameStart,
    Game,
    GameImages,
    Penalty,
    OrderCoins,
    DisputedGame,
    GameWinnerLoose
)
# Register your models here.


class UserInfoInline(admin.StackedInline):
    model = User_info
    can_delete = False
    fk_name='user'
    extra = 1
    max_num = 1
    min_num = 1
    

class userinfoAdmin(admin.ModelAdmin):
    fields = ["user","whatsapp_number","available_coins","term_condition","otp","is_verified","referral_by"]

    list_display = ["user","whatsapp_number","available_coins","term_condition","otp","is_verified","referral_by"]
    search_fields = ["user", "whatsapp_number"]
    list_filter = ["added_on", "is_verified"]
    
      


class BetTransactionInline(admin.TabularInline):
    model = BetTransaction
    can_delete = False
    fk_name = 'user'
    extra = 1


class LudoUserAdmin(UserAdmin):
    inlines = (UserInfoInline, BetTransactionInline)
    list_select_related = ('agreement',)

    def get_whatsapp_number(self, instance):
        return instance.agreement.whatsapp_number

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(LudoUserAdmin, self).get_inline_instances(request, obj)


class Contact_UsAdmin(admin.ModelAdmin):
    fields = ["contact_number","name","subject","message"]

    list_display = ["id", "name", "contact_number", "subject", "message", "added_on"]
    search_fields = ["name", "contact_number"]
    list_filter = ["added_on", "name"]
    list_editable = ["name"]


class Add_coinsAdmin(admin.ModelAdmin):
    fields = ["id", "name", "transectionid", "amount"]


class Sell_coinsAdmin(admin.ModelAdmin):
    fields = ["id", "name", "", "message"]



@admin.register(BetTransaction)
class BetTransactionAdmin(admin.ModelAdmin):
    fields = ['user', 'coins', 'game_name', 'transaction_date', 'transaction_status']


UserAdmin.list_display = ('username', 'last_name', 'email', 'get_whatsapp_number', 'is_active')

admin.site.unregister(User)
admin.site.register(User, LudoUserAdmin)

admin.site.register(Contact_Us, Contact_UsAdmin)
admin.site.register(User_info, userinfoAdmin)

admin.site.register(Add_coins, Add_coinsAdmin)
admin.site.register(Sell_coins, Sell_coinsAdmin)


admin.site.register(Game)
admin.site.register(GameImages)


admin.site.register(GameStart)
# admin.site.register(Game)

admin.site.register(OrderCoins)
admin.site.register(Penalty)
admin.site.register(DisputedGame)
admin.site.register(GameWinnerLoose)