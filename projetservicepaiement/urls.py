"""projetservicepaiement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app.views import CreatePayment, PaymentList, ValidationPayment, PaymentAccepted

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', PaymentList.as_view(), name='home'),
    path('paymentForm/', CreatePayment.as_view(), name='payment_form'),
    path('paymentList/', PaymentList.as_view(), name='payment_list'),
    path('PaymentAccepted/<int:pk>', PaymentAccepted.as_view(), name='payment_accepted'),
    path('ValidationPayment/', ValidationPayment.as_view())
]
