from django.urls import path
from Appointments import views
from Appointments.views import PatientCreate
from django.conf.urls import url

urlpatterns = [
    path('', PatientCreate.as_view(), name='home'),
    path('charge/', views.charge, name='charge'),
    path('ajax/load-cities/', views.load_time_slots, name='ajax_load_time_slots'),
    path('patient/', views.patient_view, name='p_view'),
    url(r'^new/(?P<start_time>\d{2}:\d{2}:\d{2})/(?P<day_date>\d{4}-\d{2}-\d{2})/$', views.create_event,name='new_event'),
    url(r'^appointment/(?P<pk>\d+)/$', views.appointment_detail, name='appointment-detail'),
]
