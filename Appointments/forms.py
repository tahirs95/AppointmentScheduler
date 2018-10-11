from django import forms
from .models import TimeSlots, Patient


class DateInput(forms.DateInput):
    input_type = 'date'


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ('patient_name','phone_number','email','event_date','start')
        widgets = {
            'event_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['start'].queryset = TimeSlots.objects.none()

        if 'event_date' in self.data:
            try:
                event_id = self.data.get('event_date')
                # event = Event.objects.get(pk=event_id)
                self.fields['start'].queryset = TimeSlots.objects.filter(event__event_date=event_id, event__available=True)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['start'].queryset = self.instance.timeslot_set



