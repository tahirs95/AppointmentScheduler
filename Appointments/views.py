from .models import TimeSlots, Event, Patient
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
import stripe
from .forms import PatientForm
from django.views.generic import CreateView
from .send_mail import email_user
import datetime

stripe.api_key = settings.STRIPE_SECRET_KEY


def charge(request):  # new
    change = Patient.objects.create(
        event_date=request.POST.get('event_date'),
        patient_name=request.POST.get('patient_name'),
        phone_number=request.POST.get('phone_number'),
        email=request.POST.get('email'),
        start=TimeSlots.objects.filter(id=request.POST.get('start'))[0])
    change.save()
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=5000,
            currency='usd',
            description='Book your appointment',
            source=request.POST['stripeToken']
        )
    change.paid = True
    change.save()
    email_user(change.email, change.patient_name, change.event_date, change.start)
    return render(request, 'charge.html')


class PatientCreate(CreateView):
    form_class = PatientForm
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
    q = Patient.objects.filter(paid=True)
    context = {'q_list': q}
    return render(request, template_name, context)


def appointment_detail(request, pk):
    detail = Patient.objects.get(pk=pk)
    context = {
        'detail': detail,
    }
    return render(request, 'appointment_detail.html', context)
