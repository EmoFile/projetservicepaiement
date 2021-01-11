from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from app.models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        # exclude = []
        exclude = ['date', 'state']

    amount = forms.DecimalField(max_value=9999.99,
                                widget=widgets.TextInput(
                                    attrs={'placeholder': 'Enter the amount'}))
    cardNumber = forms.IntegerField(widget=widgets.TextInput(
                                        attrs={'placeholder': 'Enter Card number'}))

    def clean_amount(self):
        try:
            return int(float(self.cleaned_data['amount']) * 100)
        except ValueError:
            self.add_error('amount', '')
            return None
