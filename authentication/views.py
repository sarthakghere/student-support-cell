from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User
from .forms import LoginForm, StaffForm

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'admin':
                return redirect('authentication:admin_dashboard')
            elif user.role == 'staff':
                return redirect('authentication:staff_dashboard')
            else:
                messages.error(request, "Unauthorized access.")
                return redirect('authentication:login')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'authentication/login.html', {'form': LoginForm()})

@login_required(login_url='authentication:login')
def logout_view(request):
    logout(request)
    return redirect('authentication:login')

@login_required(login_url='authentication:login')
@user_passes_test(is_admin, login_url='authentication:login')
def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect(request, 'authentication:login')    
    return render(request, 'authentication/admin_dashboard.html')

@login_required(login_url='authentication:login')
def staff_dashboard(request):
    if not request.user.is_authenticated:
        return redirect(request, 'authentication:login')   
    return render(request, 'authentication/staff_dashboard.html')

@login_required(login_url='authentication:login')
@user_passes_test(is_admin, login_url='authentication:login')
def staff_management(request):
    staff = User.objects.filter(role='staff')
    return render(request, 'authentication/staff/manage_options.html', {'staffs': staff})

@login_required(login_url='authentication:login')
@user_passes_test(is_admin, login_url='authentication:login')
def view_staff(request, pk):
    staff = User.objects.get(pk=pk, role='staff')
    return render(request, 'authentication/staff/view_staff.html', {'staff': staff})

@login_required(login_url='authentication:login')
@user_passes_test(is_admin, login_url='authentication:login')
def add_staff(request):
    form = StaffForm()  # Initialize the form at the beginning

    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')

            if password == confirm_password:
                user = User.objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    role='staff'
                )
                messages.success(request, "Staff added successfully!")
                return redirect('authentication:add_staff')
            else:
                messages.error(request, "Passwords do not match.")

    return render(request, 'authentication/staff/add_staff.html', {'form': form})


@login_required(login_url='authentication:login')
@user_passes_test(is_admin, login_url='authentication:login')
def delete_staff(request, pk):
    staff = get_object_or_404(User, id=pk, role='staff')
    staff.delete()
    return redirect('authentication:manage_staff')

@login_required(login_url='authentication:login')
@user_passes_test(is_admin, login_url='authentication:login')
def edit_staff(request, pk):
    staff = get_object_or_404(User, id=pk, role='staff')

    if request.method == "POST":
        # Update Staff User Details
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        staff.first_name = first_name
        staff.last_name = last_name
        staff.email = request.POST.get('email')
        staff.save()

        messages.success(request, "Student information updated successfully!")
        return redirect('authentication:manage_staff')  # Redirect to the student list page

    return render(request, 'authentication/staff/edit_staff.html', {'staff': staff})


