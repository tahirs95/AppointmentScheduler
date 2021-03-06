# Generated by Django 2.0.9 on 2018-10-08 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.DateField()),
                ('available', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Event',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('event_date', models.DateField(null=True)),
                ('patient_ID', models.AutoField(primary_key=True, serialize=False)),
                ('patient_name', models.CharField(blank=True, max_length=60, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=60, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('event', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Appointments.Event')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.TimeField(blank=True, null=True)),
                ('end', models.TimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['start'],
            },
        ),
        migrations.AddField(
            model_name='patient',
            name='start',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Appointments.TimeSlots', verbose_name='Slot time'),
        ),
        migrations.AddField(
            model_name='event',
            name='start',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Appointments.TimeSlots', verbose_name='Slot Time'),
        ),
    ]
