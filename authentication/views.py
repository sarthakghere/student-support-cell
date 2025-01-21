from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import LoginForm

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


def logout_view(request):
    logout(request)
    return redirect('authentication:login')

@login_required(login_url='authentication:login')
def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect(request, 'authentication:login')    
    return render(request, 'authentication/admin_dashboard.html')

@login_required(login_url='authentication:login')
def staff_dashboard(request):
    if not request.user.is_authenticated:
        return redirect(request, 'authentication:login')   
    return render(request, 'authentication/staff_dashboard.html')