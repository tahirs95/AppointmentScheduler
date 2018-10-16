from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse


class TimeSlots(models.Model):
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ['start']

    def __str__(self):
        return '%s - %s' % (self.start.strftime("%I:%M %p"), self.end.strftime("%I:%M %p"))


class Event(models.Model):
    event_date = models.DateField()
    start = models.ForeignKey(TimeSlots, on_delete=models.CASCADE, verbose_name='Slot Time', null=True)
    available = models.BooleanField(default=True)

    class Meta:
        verbose_name = u'Event'
        verbose_name_plural = u'Event'

    def __str__(self):
        return str(self.event_date)

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.pk])
        return u'<a href="%s">%s</a>' % (url, str(self.start))


class Patient(models.Model):
    event_date = models.DateField(null=True)
    patient_ID = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=60, null=True, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    email = models.EmailField()
    event = models.OneToOneField(Event, on_delete=models.CASCADE, null=True, blank=True)
    start = models.ForeignKey(TimeSlots, on_delete=models.CASCADE, null=True, verbose_name='Slot time')
    paid = models.BooleanField(default=False)
    skype_key = models.CharField(max_length=60, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('appointment-detail', args=[str(self.patient_ID)])

    def save(self, *args, **kwargs):
        self.event = Event.objects.get(event_date=self.event_date, start=self.start)
        change = Event.objects.get(pk=self.event.pk)
        change.available = False
        change.save()
        super(Patient, self).save(*args, **kwargs)


