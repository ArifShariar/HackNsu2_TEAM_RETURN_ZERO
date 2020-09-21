from django import forms

class orderForm(forms.Form):
    amount = forms.IntegerField(required=True)


class deliveredForm(forms.Form):
    delivered = forms.BooleanField()

