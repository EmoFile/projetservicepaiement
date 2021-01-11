from django.views.generic import CreateView, ListView

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
