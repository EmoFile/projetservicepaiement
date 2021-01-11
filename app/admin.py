from django.contrib import admin

# Register your models here.
from app.models.payment import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('date',
                    'amount',
                    'state')
    list_display_links = list_display


admin.site.register(Payment, PaymentAdmin)
