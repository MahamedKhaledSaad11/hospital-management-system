# 🏥 Shefaa Hospital Management System

![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap)
![Status](https://img.shields.io/badge/Status-Deployed-success?style=for-the-badge)

> A comprehensive web-based platform designed to bridge the gap between patients, doctors, and hospital administration, streamlining the process of booking appointments and managing medical records.

🔗 **Live Demo:** [Insert Your PythonAnywhere Link Here](https://mohamedkhaledsaad.pythonanywhere.com/)

---

## 📖 Table of Contents
- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Screenshots](#-screenshots)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)

---

## 📝 About the Project

**Shefaa Hospital System** is a full-stack web application built to digitize hospital operations. It solves the problem of manual booking and scattered medical records by providing a centralized system where:
- **Patients** can easily book appointments and view their history.
- **Doctors** can manage their schedules and diagnose patients.
- **Admins** have full control over the system's users and data.

The system emphasizes security, data validation, and a user-friendly interface using modern web technologies.

---

## ✨ Key Features

### 👤 Patient Module
- **Secure Registration:** Validates 11-digit phone numbers and professional email formats (@xxx.com).
- **Smart Booking:** Prevents booking in the past or double-booking slots.
- **Mock Payment Gateway:** Simulates secure credit card transactions to confirm appointments.
- **Medical History:** View past diagnoses and prescriptions added by doctors.
- **Profile Management:** Update personal and contact details.

### 👨‍⚕️ Doctor Module
- **Dashboard:** View upcoming appointments filtered by date.
- **Patient Management:** Access a list of patients who have booked appointments.
- **Diagnosis System:** Add medical records (Diagnosis & Treatment), which automatically marks appointments as "Completed".
- **Specialization Filtering:** Doctors are categorized by department (Cardiology, Neurology, etc.).

### 🛠️ Admin Module
- **Dashboard Analytics:** Live statistics on total doctors, patients, and appointments.
- **User Management:** Add/Delete Doctors and Delete Patients with strict validation rules.
- **Appointment Control:** View all system appointments and emergency cancellation capabilities.
- **Security:** Role-based access control prevents unauthorized access.

---

## 💻 Tech Stack

- **Backend:** Django (Python Framework)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5 (Responsive Design)
- **Database:** SQLite (Development/Production on PythonAnywhere)
- **Authentication:** Django Auth System (Customized User Model)
- **Deployment:** PythonAnywhere

---



## 🚀 Installation & Setup

Follow these steps to run the project locally on your machine.

### Prerequisites
- Python 3.10+ installed
- Git installed

### Steps

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/yourusername/hospital-management-system.git](https://github.com/yourusername/hospital-management-system.git)
   cd hospital-management-system