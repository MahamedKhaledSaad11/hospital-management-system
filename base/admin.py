from django.contrib import admin
from .models import User, Patient, Doctor, Appointment, MedicalHistory

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(MedicalHistory)