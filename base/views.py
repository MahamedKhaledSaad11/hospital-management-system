from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import User, Patient, Doctor, Appointment, MedicalHistory
from django.contrib import messages
from datetime import datetime, date as date_obj
# --- Authentication Views ---

def home(request):
    return render(request, 'base/home.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect based on role
            if user.is_patient:
                return redirect('patient_dashboard')
            elif user.is_doctor:
                return redirect('doctor_dashboard')
            elif user.is_admin:
                return redirect('admin_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'base/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

@csrf_protect
def signup_patient(request):
    values = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        values = request.POST
        error_msg = None
        if len(phone) != 11 or not phone.isdigit():
            error_msg = '❌ Phone number must be exactly 11 digits!'
        elif not email.endswith('.com') or '@' not in email:
            error_msg = '❌ Invalid email format! Must contain @ and end with .com'
        elif User.objects.filter(username=username).exists():
            error_msg = '❌ Username already taken!'
        elif User.objects.filter(email=email).exists():
            error_msg = '❌ This email is already registered!'
        elif Patient.objects.filter(phone_number=phone).exists() or Doctor.objects.filter(phone_number=phone).exists():
            error_msg = '❌ This phone number is already in use!'
        if error_msg:
            messages.error(request, error_msg)
            return render(request, 'base/signup.html', {'values': values})
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = fname
        user.last_name = lname
        user.is_patient = True
        user.save()
        Patient.objects.create(user=user, age=age, phone_number=phone, address=address)  
        messages.success(request, '✅ Account created! Please login.')
        return redirect('login')
    return render(request, 'base/signup.html')

@login_required(login_url='login')
def patient_dashboard(request):
    if not request.user.is_patient:
        return redirect('home')
    patient = request.user.patient
    appointments = Appointment.objects.filter(patient=patient).order_by('-date', '-time')
    context = {
        'appointments': appointments,
        'patient': patient
    }
    return render(request, 'base/patient_dashboard.html', context)

@login_required(login_url='login')
def book_appointment(request):
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        date_str = request.POST.get('date') # Returns string "YYYY-MM-DD"
        time_str = request.POST.get('time') # Returns string "HH:MM"
        specialization = request.POST.get('specialization')
        booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        booking_time = datetime.strptime(time_str, "%H:%M").time()
        current_date = datetime.now().date()
        current_time = datetime.now().time()
        if booking_date < current_date:
            messages.error(request, ' You cannot book a date in the past!')
            return redirect('book_appointment')
        if booking_date == current_date and booking_time < current_time:
            messages.error(request, ' That time has already passed today!')
            return redirect('book_appointment')
        doctor = Doctor.objects.get(pk=doctor_id)
        if Appointment.objects.filter(doctor=doctor, date=date_str, time=time_str).exists():
            messages.error(request, ' This time slot is already booked! Please choose another time.')
            return redirect('book_appointment')
        new_appointment = Appointment.objects.create(
            patient=request.user.patient,
            doctor=doctor,
            date=date_str,
            time=time_str,
            specialization=specialization,
            status='Pending'
        )
        return redirect('payment_page', appt_id=new_appointment.id)
    context = {'doctors': doctors}
    return render(request, 'base/book_appointment.html', context)

@login_required(login_url='login')
def medical_history(request):
    if not request.user.is_patient:
        return redirect('home')
    history_records = MedicalHistory.objects.filter(patient=request.user.patient).order_by('-date')
    context = {'history': history_records}
    return render(request, 'base/medical_history.html', context)

@login_required(login_url='login')
def patient_profile(request):
    if not request.user.is_patient:
        return redirect('home')
    patient = request.user.patient
    if request.method == 'POST':
        patient.phone_number = request.POST.get('phone')
        patient.address = request.POST.get('address')
        patient.age = request.POST.get('age')
        patient.save()
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('patient_profile')
    context = {'patient': patient}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def doctor_dashboard(request):
    if not request.user.is_doctor:
        return redirect('home')
    doctor = request.user.doctor
    today = date_obj.today()
    upcoming_appointments = Appointment.objects.filter(
        doctor=doctor, 
        date__gte=today
    ).order_by('date', 'time')
    my_patient_ids = Appointment.objects.filter(doctor=doctor).values_list('patient_id', flat=True).distinct()
    my_patients = Patient.objects.filter(user_id__in=my_patient_ids)
    context = {
        'appointments': upcoming_appointments,
        'patients': my_patients,
        'doctor': doctor
    }
    return render(request, 'base/doctor_dashboard.html', context)

@login_required(login_url='login')
def add_medical_history(request, patient_id):
    if not request.user.is_doctor:
        return redirect('home')
    user_patient = User.objects.get(pk=patient_id)
    patient = user_patient.patient
    if request.method == 'POST':
        diagnosis = request.POST.get('diagnosis')
        treatment = request.POST.get('treatment')
        MedicalHistory.objects.create(
            patient=patient,
            doctor=request.user.doctor,
            diagnosis=diagnosis,
            treatment=treatment
        )
        Appointment.objects.filter(
            patient=patient, 
            doctor=request.user.doctor, 
            status='Confirmed'
        ).update(status='Completed')
        messages.success(request, f'Diagnosis added and appointment marked Completed!')
        return redirect('doctor_dashboard')
    context = {'patient': patient}
    return render(request, 'base/add_history.html', context)

@login_required(login_url='login')
def admin_dashboard(request):
    if not (request.user.is_admin or request.user.is_superuser):
        return redirect('home')
    doctor_count = Doctor.objects.count()
    patient_count = Patient.objects.count()
    appointment_count = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='Pending').count()

    doctors = Doctor.objects.all()

    context = {
        'doctor_count': doctor_count,
        'patient_count': patient_count,
        'appointment_count': appointment_count,
        'pending_appointments': pending_appointments,
        'doctors': doctors
    }
    return render(request, 'base/admin_dashboard.html', context)

@login_required(login_url='login')
def admin_add_doctor(request):
    if not (request.user.is_admin or request.user.is_superuser):
        return redirect('home')
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        specialization = request.POST.get('specialization')
        degree = request.POST.get('degree')
        salary = request.POST.get('salary')
        dept_id = request.POST.get('dept_id')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        if len(phone) != 11 or not phone.isdigit():
            messages.error(request, ' Phone number must be exactly 11 digits!')
            return redirect('admin_add_doctor')
        if not email.endswith('.com') or '@' not in email:
            messages.error(request, ' Invalid email format! Must end with .com')
            return redirect('admin_add_doctor')
        if User.objects.filter(username=username).exists():
            messages.error(request, ' Username already taken!')
            return redirect('admin_add_doctor')
        if User.objects.filter(email=email).exists():
            messages.error(request, ' Email already registered!')
            return redirect('admin_add_doctor')
        if Doctor.objects.filter(phone_number=phone).exists() or Patient.objects.filter(phone_number=phone).exists():
            messages.error(request, ' Phone number already in use!')
            return redirect('admin_add_doctor')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = fname
        user.last_name = lname
        user.is_doctor = True
        user.save()
        Doctor.objects.create(
            user=user, specialization=specialization, degree=degree, salary=salary,
            phone_number=phone, department_id=dept_id, age=age, gender=gender
        )
        messages.success(request, f' Dr. {lname} added successfully!')
        return redirect('admin_dashboard')

    return render(request, 'base/add_doctor.html')

@login_required(login_url='login')
def delete_doctor(request, pk):
    if not request.user.is_admin:
        return redirect('home') 
    doctor = Doctor.objects.get(id=pk)
    user = doctor.user
    user.delete()
    messages.success(request, 'Doctor deleted successfully.')
    return redirect('admin_dashboard')

@login_required(login_url='login')
def delete_patient(request, pk):
    if not request.user.is_admin:
        return redirect('home')        
    patient = Patient.objects.get(pk=pk)
    user = patient.user
    user.delete()
    messages.success(request, 'Patient deleted successfully.')
    return redirect('admin_dashboard')

@login_required(login_url='login')
def payment_page(request, appt_id):
    appointment = Appointment.objects.get(id=appt_id)
    if request.method == 'POST':
        appointment.status = 'Confirmed'
        appointment.save()
        messages.success(request, ' Payment Successful! Your appointment is now Confirmed.')
        return redirect('patient_dashboard')
    context = {'appointment': appointment}
    return render(request, 'base/payment.html', context)

@login_required(login_url='login')
def admin_appointments(request):
    if not (request.user.is_admin or request.user.is_superuser):
        return redirect('home')
    appointments = Appointment.objects.exclude(status='Cancelled').order_by('-date', '-time')
    return render(request, 'base/admin_appointments.html', {'appointments': appointments})

@login_required(login_url='login')
def cancel_appointment_admin(request, pk):
    if not (request.user.is_admin or request.user.is_superuser):
        return redirect('home')
    appointment = Appointment.objects.get(id=pk)
    if appointment.status == 'Cancelled':
        messages.warning(request, 'Appointment is already cancelled.')
    else:
        appointment.status = 'Cancelled'
        appointment.save()
        messages.success(request, 'Appointment has been cancelled due to emergency.')
    return redirect('admin_appointments')