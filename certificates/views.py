from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
def is_authorized(user):
    return user.is_authenticated and (user.role == 'admin' or user.role == 'staff')


@login_required(login_url='authentication:login')
@user_passes_test(is_authorized, login_url='authentication:login')
def certificates(request):
    return render(request, 'certificates/certificates_home.html')