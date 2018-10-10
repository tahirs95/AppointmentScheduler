from .models import TimeSlots, Event, Patient
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
import stripe
from .forms import PatientForm
from django.views.generic import CreateView

stripe.api_key = settings.STRIPE_SECRET_KEY


def charge(request):  # new
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=5000,
            currency='usd',
            description='Book your appointment',
            source=request.POST['stripeToken']
        )
        return render(request, 'charge.html')


class PatientCreate(CreateView):
    form_class = PatientForm
    success_url = '/admin/'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):  # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


def load_time_slots(request):
    event_id = request.GET.get('event_date')
    time_slots = TimeSlots.objects.filter(event__event_date=event_id, event__available=True)
    return render(request, 'dropdown_list_options.html', {'time_slots': time_slots})


def create_event(request, start_time, day_date):
    time_slot = TimeSlots.objects.get(start=start_time)
    Event.objects.create(event_date=day_date, start=time_slot)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def patient_view(request):
    template_name = 'patient_dashboard.html'
    q = Patient.objects.all()
    context = { 'q_list': q}
    return render(request, template_name, context)