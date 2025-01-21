from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student

# Create your views here.
@login_required(login_url='authentication:login')
def student_management(request):
    students = Student.objects.all()
    return render(request, 'students/manage_options.html', {'students': students})


@login_required(login_url='authentication:login')
def view_student(request, pk):
    student = Student.objects.get(pk=pk)
    return render(request, 'students/view_student.html', {'student': student})

def edit_student(request, pk):
    student = get_object_or_404(Student, id=pk)

    if request.method == "POST":
        # Update Student User Details
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student.user.first_name = first_name
        student.user.last_name = last_name
        student.user.save()

        # Update Student Details
        student.prn = request.POST.get('prn')
        student.dob = request.POST.get('dob')
        student.gender = request.POST.get('gender')
        student.phone_number = request.POST.get('phone_number')
        student.program = request.POST.get('program')
        student.semester = request.POST.get('semester')
        student.street_address = request.POST.get('street_address')
        student.city = request.POST.get('city')
        student.state = request.POST.get('state')
        student.pincode = request.POST.get('pincode')
        student.country = request.POST.get('country')
        student.save()

        messages.success(request, "Student information updated successfully!")
        return redirect('students:manage_students')  # Redirect to the student list page

    return render(request, 'students/edit_student.html', {'student': student})

def delete_student(request, pk):
    student = get_object_or_404(Student, id=pk)
    student.delete()
    return redirect('students:manage_students')