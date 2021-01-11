from django.core.validators import MinValueValidator, MinLengthValidator, MaxLengthValidator
from django.db import models


class Payment(models.Model):
    PENDING = 'Pending'
    ACCEPTED = 'Accepted'
    VALIDATED = 'Validated'
    STATE_CHOICES = [
        (PENDING, 'Common'),
        (ACCEPTED, 'Rare'),
        (VALIDATED, 'Epic'),
    ]
    state = models.CharField(choices=STATE_CHOICES,
                             default=PENDING)
    cardNumber = models.CharField(validators=[MinLengthValidator(16), MaxLengthValidator(16)],
                                  default='0000000000000000',
                                  blank=False,
                                  null=False)
    date = models.DateTimeField(blank=True,
                                null=True)
    amount = models.BigIntegerField(validators=[MinValueValidator(0)],
                                    blank=False,
                                    null=False)
