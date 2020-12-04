from django import forms
from ludoapp.models import Add_coins,Sell_coins

class add_Coins_form(forms.ModelForm):
    class Meta:
        model = Add_coins
        
        # exclude = ["product_name","details"]
        fields = ["transection_id","amount"]

class sell_coin_form(forms.ModelForm):
    class Meta:
        model = Sell_coins
        
        # exclude = ["product_name","details"]
        fields = ["paytm_number","amount"]