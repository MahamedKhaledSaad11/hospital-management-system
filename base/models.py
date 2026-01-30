from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Custom User Model
# We extend the default user to handle Admin, Doctor, and Patient roles in one login system.
class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_patient = models.BooleanField('Is patient', default=False)
    is_doctor = models.BooleanField('Is doctor', default=False)

# 2. Patient Model
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    age = models.IntegerField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    
    def __str__(self):
        return self.user.username

# 3. Doctor Model
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    degree = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    department_id = models.CharField(max_length=50) # Can be used as a room number or dept code
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    age = models.IntegerField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} ({self.specialization})"

# 4. Appointment Model
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments')
    date = models.DateField()
    time = models.TimeField()
    specialization = models.CharField(max_length=100) # Snapshot of what they booked for
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Unique constraint: A doctor cannot have two appointments at the exact same date and time
        unique_together = ('doctor', 'date', 'time')

    def __str__(self):
        return f"{self.patient.user.username} with {self.doctor.user.last_name} on {self.date} at {self.time}"

# 5. Medical History Model
class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_history')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True) # If doctor is deleted, history remains
    diagnosis = models.TextField()
    treatment = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"History for {self.patient.user.username} - {self.date}"