from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User
from .forms import LoginForm, StaffForm, StaffEditForm
from students.models import Certificate

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None and user.role in (User.RoleChoices.ADMIN, User.RoleChoices.STAFF):
                login(request, user)
                if user.role == User.RoleChoices.ADMIN:
                    return redirect('authentication:admin_dashboard')
                elif user.role == User.RoleChoices.STAFF:
                    return redirect('certificates:certificates_home')
            else:
                form.add_error('email', "Invalid email or password")
    return render(request, 'authentication/login.html', {'form': form})

@login_required(login_url='authentication:login')
def logout_view(request):
    logout(request)
    request.session.flush()
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
    form = StaffForm()  # Initialize the form

    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            full_name = form.cleaned_data.get('full_name')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "A staff member with this email already exists.")

            elif password != confirm_password:
                messages.error(request, "Passwords do not match.")
            else:
                # Create staff user
                user = User.objects.create_user(
                    email=email,
                    full_name=full_name,
                    password=password,
                    role='staff'
                )
                messages.success(request, "Staff added successfully!")
                return redirect('authentication:manage_staff')

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
    data = {
        'full_name': staff.full_name,
        'email': staff.email,
    }
    form = StaffEditForm(initial=data)

    if request.method == "POST":
        form = StaffEditForm(request.POST)
        # Update Staff User Details
        if form.is_valid():

            full_name = form.cleaned_data.get('full_name')
            email = form.cleaned_data.get('email')

            if User.objects.filter(email=email).exclude(id=staff.id).exists():
                form.add_error('email', "This email is already in use.")
                return render(request, 'authentication/staff/edit_staff.html', {'staff': staff, 'form': form})
            
            staff.full_name = full_name
            staff.email = email
            staff.save()
            messages.success(request, "Staff information updated successfully!")

            return redirect('authentication:manage_staff')  # Redirect to the staff list page

    return render(request, 'authentication/staff/edit_staff.html', {'staff': staff, 'form': form})

@login_required(login_url='authentication:login')
def credits(request):
    return render(request, 'authentication/credits.html')

@login_required(login_url='authentication:login')
@user_passes_test(is_admin, login_url='authentication:login')
def approve__duplicate_certificate(request):
    certificates = Certificate.objects.filter(approval_status=Certificate.StatusChoices.PENDING)
    return render(request, 'authentication/approve_duplicate_certificates.html', {'certificates': certificates})