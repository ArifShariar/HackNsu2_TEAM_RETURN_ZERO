from django import forms

class orderForm(forms.Form):
    order_quantity = forms.IntegerField(required=True)
    
class deliveredForm(forms.Form):
    delivered = forms.BooleanField()
