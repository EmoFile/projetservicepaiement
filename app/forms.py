from itertools import count

from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from app.models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['date', 'state']

    amount = forms.DecimalField(max_value=9999.99,
                                widget=widgets.TextInput(
                                    attrs={'placeholder': 'Enter the amount'}))
    card_number = forms.IntegerField(widget=widgets.TextInput(
                                        attrs={'placeholder': 'Enter Card number'}))

    def clean_amount(self):
        try:
            return int(float(self.cleaned_data['amount']) * 100)
        except ValueError:
            self.add_error('amount', 'the amount should be a decimal with 2 digit after comma')

    def clean_card_number(self):
        data = self.cleaned_data['card_number']
        if len(str(data)) != 16 or data.__class__ is not int:
            self.add_error('card_number', 'the card number should be a 16 digit number')
        return data
