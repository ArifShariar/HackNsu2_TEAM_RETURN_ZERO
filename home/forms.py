from django import forms

class orderForm(forms.Form):
    amount = forms.IntegerField(required=True)
