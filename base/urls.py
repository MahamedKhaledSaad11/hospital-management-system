from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_patient, name='signup_patient'),
    path('payment/<int:appt_id>/', views.payment_page, name='payment_page'),

    # Patient Routes
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/book_appointment/', views.book_appointment, name='book_appointment'),
    path('patient/history/', views.medical_history, name='medical_history'),
    path('patient/profile/', views.patient_profile, name='patient_profile'),

    # Doctor Routes
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/add_history/<int:patient_id>/', views.add_medical_history, name='add_medical_history'),
    
    # Admin Routes
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_doctor/', views.admin_add_doctor, name='admin_add_doctor'),
    path('delete_doctor/<int:pk>/', views.delete_doctor, name='delete_doctor'),
    path('delete_patient/<int:pk>/', views.delete_patient, name='delete_patient'),
    path('admin_appointments/', views.admin_appointments, name='admin_appointments'),
    path('cancel_appointment/<int:pk>/', views.cancel_appointment_admin, name='cancel_appointment_admin'),
]