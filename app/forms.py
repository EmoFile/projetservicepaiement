from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from app.models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        # exclude = []
        fields = ['date', 'state']

    amount = forms.DecimalField(max_value=9999.99,
                                max_digits=2,
                                widget=widgets.TextInput(
                                    attrs={'placeholder': 'Enter the amount'}))
    cardNumber = forms.IntegerField(min_length=16,
                                    max_length=16,
                                    widget=widgets.TextInput(
                                        attrs={'placeholder': 'Enter Card number'}))
