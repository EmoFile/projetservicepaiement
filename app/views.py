from django.views.generic import CreateView, ListView
import requests
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from app.forms import PaymentForm
from app.models.payment import Payment


class CreatePayment(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'paymentForm.html'


class PaymentList(ListView):
    template_name = 'paymentList.html'
    model = Payment
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = Payment.objects.all()
        return context


class ValidationPayment(generic.View):
    http_method_names = ['post']

    @method_decorator(never_cache)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.POST['id'])
        print(request.POST['amount'])
        return HttpResponse("OK")


def send_payment(*args, **kwargs):
    payment = {"id": "2", "amount": "350"}
    response = requests.post("http://127.0.0.1:8000/ValidationPayment", data=payment)
    print(response.json())

