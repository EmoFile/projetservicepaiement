import datetime
import requests
import email.utils as eut

import logging
from app.forms import PaymentForm
from app.models.payment import Payment
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt



class CreatePayment(FormView):
    success_url = reverse_lazy('payment_list')
    model = Payment
    form_class = PaymentForm
    template_name = 'paymentForm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Formulaire de paiments'
        return context

    def form_valid(self, form):
        Payment.objects.create(
            amount=form.cleaned_data['amount'],
            card_number=form.cleaned_data['card_number']
        )
        created_payment = Payment.objects.last()
        result = send_payment(id=created_payment.id, amount=created_payment.amount)
        if not result['isTrue']:
            form.add_error('card_number', result['error'])
            return super().form_invalid(form)
        return super().form_valid(form)


class PaymentList(ListView):
    template_name = 'paymentList.html'
    model = Payment
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = Payment.objects.all()
        context['title'] = 'Liste des paiments'
        return context


class ValidationPayment(generic.View):
    http_method_names = ['post']

    @method_decorator(never_cache)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print('nassim')
        print(request.POST['id'])
        print(request.POST['amount'])
        return HttpResponse("OK")


def send_payment(*args, **kwargs):
    payment = {"id": kwargs["id"], "amount": kwargs["amount"]}
    try:
        response = requests.post("http://127.0.0.1:8000/zeaefaef", json=payment)
        if response.status_code == 200:
            current_payment = get_object_or_404(Payment, id=kwargs["id"])
            current_payment.date = datetime.datetime(*eut.parsedate(response.headers._store['date'][1])[:6])
            current_payment.state = "ACCEPTED"
            current_payment.save()
            return True
        else:
            if response.status_code == 500 or response.status_code == 503:
                error = "Serveur de paiment inaccesible veuillez réessayer plus tard ou contacter un admin"
            else:
                error = "Une erreure innatendu est apparu veuillez contactez un admin"
            response.raise_for_status()
            print("Error")
    except requests.exceptions.HTTPError as e:
        print(e)
        logging.basicConfig(filename='contactServicePayment.log',
                            format='%(asctime)s - %(message)s',
                            level=logging.WARNING,
                            datefmt='%d-%b-%y %H:%M:%S')
        logging.error(f'{e} - id: {kwargs["id"]} - amount: {kwargs["amount"]}')
        return {'isTrue': False, 'error': error}
