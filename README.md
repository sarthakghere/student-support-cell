# Student Support Cell (SSC) Management System

## Description
The **Student Support Cell Management System** is a web application developed using **Django** that helps manage student data, certificates, and admin staff activities. The system supports user roles like **Admin** and **Staff**, each with specific features to facilitate student record management and certificate issuance.

---

## Features

### Admin Features
- Add, view, update, and delete student records.
- Bulk upload students via CSV or Excel.
- Approve and manage certificate requests (e.g., Transfer Certificates and Bonafide Certificates).
- Manage staff user accounts.

### Staff Features
- View student records.
- Generate and manage certificates like Transfer Certificates (TC) and Bonafide Certificates.
- Submit requests for duplicate certificates for admin approval.

---

## Technology Stack

- **Backend**: Django (with built-in authentication system)
- **Frontend**: Django Templates, Bootstrap, Vanilla JavaScript
- **Database**: MySQL

---

## Installation

### Prerequisites
- Python 3.x
- MySQL Database
- pip (Python package manager)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/student-support-cell.git
   cd student-support-cell
   ```

2. **Create a virtual environment**:
   ```bash
   pipenv shell
   ```

3. **Install dependencies**:
   ```bash
   pipenv install
   ```

4. **Set up MySQL database**:
   - Create a database in MySQL:
     ```sql
     CREATE DATABASE student_support_cell;
     ```

   - Update your Django project’s `settings.py` to connect to MySQL:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'student_support_cell',
             'USER': 'your_mysql_user',
             'PASSWORD': 'your_mysql_password',
             'HOST': 'localhost',
             'PORT': '3306',
         }
     }
     ```

5. **Migrate the database**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. Visit the application in your browser:
   ```bash
   http://127.0.0.1:8000
   ```

---