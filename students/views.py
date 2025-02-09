from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import Student
from authentication.models import User
from .forms import StudentForm, EditStudentForm
from dotenv import load_dotenv
import os
import pandas as pd
load_dotenv()

# Create your views here.
@login_required(login_url='authentication:login')
def student_management(request):
    students = Student.objects.all()
    return render(request, 'students/manage_options.html', {'students': students})

@login_required(login_url='authentication:login')
def view_student(request, pk):
    student = Student.objects.get(pk=pk)
    return render(request, 'students/view_student.html', {'student': student})

@login_required(login_url='authentication:login')
def edit_student(request, pk):
    student = get_object_or_404(Student, id=pk)
    data = {
        'prn': student.prn,
        'erp': student.erp,
        'full_name': student.user.full_name,
        'phone_number': student.phone_number,
        'email': student.user.email,
        'abc_id': student.abc_id,
        'gender' : student.gender,
        'dob': student.dob,

        'alternate_phone_number': student.alternate_phone_number,
        'fathers_name': student.fathers_name,
        'fathers_contact': student.fathers_contact,
        'mothers_name': student.mothers_name,
        'mothers_contact': student.mothers_contact,

        'category': student.category,
        'disability': student.disability,
        'cet_rank': student.cet_rank,
        'special_quota': student.special_quota,
        'family_income': student.family_income,
        'previous_academic_stream': student.previous_academic_stream,

        'program': student.program,
        'semester': student.semester,
        'course_start_year': student.course_start_year,
        'course_duration': student.course_duration,

        'permanent_address': student.permanent_address,
        'current_address': student.current_address,
        'state': student.state,
    }
    
    form = EditStudentForm(initial=data)


    if request.method == "POST":
        form = EditStudentForm(request.POST)
        if not form.is_valid():
            messages.error(request, "There was an error with the form. Please correct it.")
            return render(request, 'students/edit_student.html', {'student': student, 'form': form})
        
        # Update Student User Details
        full_name = form.cleaned_data.get('full_name')
        student.user.first_name = full_name
        student.user.save()

        # Update Student Details
        student.dob = form.cleaned_data.get('dob')
        student.gender = form.cleaned_data.get('gender')
        student.phone_number = form.cleaned_data.get('phone_number')
        
        student.alternate_phone_number = form.cleaned_data.get('alternate_phone_number')
        student.fathers_name = form.cleaned_data.get('fathers_name')
        student.fathers_contact = form.cleaned_data.get('fathers_contact')
        student.mothers_name = form.cleaned_data.get('mothers_name')
        student.mothers_contact = form.cleaned_data.get('mothers_contact')

        student.category = form.cleaned_data.get('category')
        student.disability = form.cleaned_data.get('disability')
        student.cet_rank = form.cleaned_data.get('cet_rank')
        student.special_quota = form.cleaned_data.get('special_quota')
        student.family_income = form.cleaned_data.get('family_income')
        
        student.program = form.cleaned_data.get('program')
        student.semester = form.cleaned_data.get('semester')
        student.course_duration = form.cleaned_data.get('course_duration')
        student.course_start_year = form.cleaned_data.get('course_start_year')

        student.permanent_address = form.cleaned_data.get('permanent_address')
        student.current_address = form.cleaned_data.get('current_address')
        student.state = form.cleaned_data.get('state')

        student.save()

        messages.success(request, "Student information updated successfully!")
        return redirect('students:manage_students')  # Redirect to the student list page

    return render(request, 'students/edit_student.html', {'student': student, 'form': form})

@login_required(login_url='authentication:login')
def delete_student(request, pk):
    student = get_object_or_404(Student, id=pk)
    student.delete()
    return redirect('students:manage_students')

@login_required(login_url='authentication:login')
def add_student(request):
    return render(request, 'students/add_student.html')

@login_required(login_url='authentication:login')
def add_single_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            prn = form.cleaned_data.get('prn')
            full_name = form.cleaned_data.get('full_name')

            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                form.add_error('email', "A student with this email already exists.")
                messages.error(request, "A student with this email already exists.")
            # Check if PRN already exists
            elif Student.objects.filter(prn=prn).exists():
                form.add_error('prn', "A student with this PRN already exists.")
                messages.error(request, "A student with this PRN already exists.")
            else:
                # Create or retrieve the User instance
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        'full_name': full_name,
                        'role': 'student',
                        'password': os.getenv('DEFAULT_STUDENT_PASSWORD'),
                    }
                )

                # Create the Student instance and associate it with the User
                student = Student.objects.create(
                    user=user,
                    prn=prn,
                    erp = form.cleaned_data.get('erp'),
                    abc_id = form.cleaned_data.get('abc_id'),
                    dob = form.cleaned_data.get('dob'),
                    gender = form.cleaned_data.get('gender'),

                    phone_number = form.cleaned_data.get('phone_number'),
                    alternate_phone_number = form.cleaned_data.get('alternate_phone_number'),
                    fathers_name = form.cleaned_data.get('fathers_name'),
                    fathers_contact = form.cleaned_data.get('fathers_contact'),
                    mothers_name = form.cleaned_data.get('mothers_name'),
                    mothers_contact = form.cleaned_data.get('mothers_contact'),

                    program = form.cleaned_data.get('program'),
                    semester = form.cleaned_data.get('semester'),
                    course_start_year = form.cleaned_data.get('course_start_year'),
                    course_duration = form.cleaned_data.get('course_duration'),

                    permanent_address = form.cleaned_data.get('permanent_address'),
                    current_address = form.cleaned_data.get('current_address'),
                    state = form.cleaned_data.get('state'),

                    category = form.cleaned_data.get('category'),
                    disability = form.cleaned_data.get('disability'),
                    cet_rank = form.cleaned_data.get('cet_rank'),
                    special_quota = form.cleaned_data.get('special_quota'),
                    family_income = form.cleaned_data.get('family_income'),
                    previous_academic_stream = form.cleaned_data.get('previous_academic_stream'),
                )

                messages.success(request, "Student added successfully!")
                return redirect('students:manage_students')  # Replace with the appropriate URL

        else:
            messages.error(request, "There was an error with the form. Please correct it.")

    else:
        form = StudentForm()

    return render(request, 'students/add_single_student.html', {'form': form})

@login_required(login_url='authentication:login')
def bulk_add_students(request):
    table_html = None
    file_name = None

    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        # Save the file temporarily
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)  # Get the absolute path
        
        try:
            # Read the Excel file
            df = pd.read_excel(file_path)
            table_html = df.to_html(classes="table table-striped table-bordered", index=False)
            file_name = filename  # Pass file name to keep track
        except Exception as e:
            return render(request, 'students/bulk_add_upload.html', {
                'error': f"Error processing the file: {e}"
            })

    return render(request, 'students/bulk_add_upload.html', {
        'table_html': table_html,
        'file_name': file_name
    })

@login_required(login_url='authentication:login')
def bulk_add_confirm(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    df = pd.read_excel(file_path)

    try:
        for index, row in df.iterrows():
            # Create or retrieve the User instance
            user, created = User.objects.get_or_create(
                email=row['email'],
                defaults={
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'role': 'student',
                    'password': os.getenv('DEFAULT_STUDENT_PASSWORD'),
                }
            )

            # Create the Student instance and associate it with the User
            student = Student.objects.create(
                user=user,
                prn=row['prn'],
                phone_number=row['phone_number'],
                dob=row['dob'],
                gender=row['gender'],
                program=row['program'],
                semester=row['semester'],
                course_start_year=row['course_start_year'],
                course_duration=row['course_duration'],
                caste=row['caste'],
                religion=row['religion'],
                nationality=row['nationality'],
                pan=row['pan'],
                aadhar=row['aadhar'],
                abc_id=row['abc_id'],
                street_address=row['street_address'],
                city=row['city'],
                state=row['state'],
                pincode=row['pincode'],
                country=row['country'],
            )
    except Exception as e:
        messages.error(request, f"Error adding students: {e}")
        return redirect('students:bulk_add_upload')
    
    else:
        messages.success(request, "Students added successfully!")
        return redirect('students:manage_students')  