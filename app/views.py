import json
import sys

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
        """

        :param kwargs:
        :return context:
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Formulaire de paiments'
        return context

    def form_valid(self, form):
        """

        :param form:
        :return form:
        """
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

    def get_context_data(self, traited_payments=None, **kwargs):
        """

        :param traited_payments:
        :return context:
        """
        if traited_payments is None:
            traited_payments = []
        context = super().get_context_data(**kwargs)
        payments = Payment.objects.all()
        for payment in payments:
            payment.amount = payment.amount / 100
            traited_payments.insert(len(traited_payments), payment)
        context['payments'] = traited_payments
        context['title'] = 'Liste des paiements'
        return context


class ValidationPayment(generic.View):
    """
    Only post can be called in this view
    """
    http_method_names = ['post']

    @method_decorator(never_cache)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Only Request with id in his JSON will work. If the ID is not existing in the base tha t will do 404 or 403
        In the production the security will check the IP (like the logg tell)
        :param request: Mandatory: the request with the POST where the ID is mandatory. if id is not existing error 404
        :return HttpResponse:
        """
        received = json.loads(request.body)
        logging.basicConfig(filename='contactValidationPayment.log',
                            format='%(asctime)s - %(message)s',
                            level=logging.WARNING,
                            datefmt='%d-%b-%y %H:%M:%S')
        if not 'id' in received:
            logging.error(f'no ID {request.META.get("REMOTE_ADDR")}')
            return HttpResponse(status=404)
        try:
            if isinstance(received['id'], int) and Payment.objects.get(id=received["id"]):
                current_payment = get_object_or_404(Payment, id=received["id"])
                current_payment.state = "Validated"
                current_payment.save()
                return HttpResponse("OK")
        except:
            e = sys.exc_info()[0]
            logging.error(f'{e}')
        logging.error(f'Error the ID is not existing - id: {received["id"]} - IP: {request.META.get("REMOTE_ADDR")}')
        return HttpResponse(status=404)


def send_payment(*args, **kwargs):
    """
    This function will send to the middleware the payment for be accepted. The middleware will response status code 202 if ok

    :key id: Mandatory: this key will be send to web service for paiment to identify the validation after
    :key moment Mandatory: this key will be send to web service for paiment.
    :return JSON{istrue Mandatory, error Optional {if n error from the request is occured} :
    """
    payment = {"id": kwargs["id"], "amount": kwargs["amount"]}
    try:
        response = requests.post("http://127.0.0.1:8000/ValidationPayment/", json=payment)
        if response.status_code == 200:
            current_payment = get_object_or_404(Payment, id=kwargs["id"])
            print(eut.parsedate_to_datetime(response.headers._store['date'][1]))
            current_payment.date = eut.parsedate_to_datetime(response.headers._store['date'][1])
            #current_payment.date = datetime.datetime(*eut.parsedate(response.headers._store['date'][1])[:6])
            current_payment.state = "Accepted"
            current_payment.save()
            return {'isTrue': True}
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
