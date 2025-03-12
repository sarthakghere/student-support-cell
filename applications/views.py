from django.shortcuts import render
from django.http import HttpResponse
from .models import StudentApplication

# Create your views here.
def list_applications(request):
    applications = StudentApplication.objects.all()
    return render(request, 'applications/list_applications.html', {'applications': applications})