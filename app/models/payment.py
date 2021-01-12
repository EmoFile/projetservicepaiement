from django.core.validators import MinValueValidator, MinLengthValidator, MaxLengthValidator, MaxValueValidator
from django.db import models


class Payment(models.Model):
    PENDING = 'Pending'
    ACCEPTED = 'Accepted'
    VALIDATED = 'Validated'
    STATE_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (VALIDATED, 'Validated'),
    ]
    state = models.CharField(max_length=20,
                             choices=STATE_CHOICES,
                             default=PENDING)
    card_number = models.CharField(max_length=16,
                                   validators=[MinLengthValidator(16), MaxLengthValidator(16)],
                                   default='0000000000000000',
                                   blank=False,
                                   null=False)
    date = models.DateTimeField(blank=True,
                                null=True)
    amount = models.BigIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)],
                                    blank=False,
                                    null=False)
