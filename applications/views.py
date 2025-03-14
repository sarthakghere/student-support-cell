from django.shortcuts import render
from .models import StudentApplication
from .generate_application import generate
from django.http import FileResponse
import os

# Create your views here.
def list_applications(request):
    applications = StudentApplication.objects.all()
    return render(request, 'applications/list_applications.html', {'applications': applications})

def view_application(request, pk):
    application = StudentApplication.objects.get(pk=pk)
    return render(request, 'applications/view_application.html', {'application': application})

def print_application(request, pk):
    application = StudentApplication.objects.get(pk=pk)
    application_data = {
        'first_name': application.student.user.first_name if application.student else application.first_name,
        'last_name': application.student.user.last_name if application.student else application.last_name,
        'prn': application.student.prn if application.student else application.prn,
        'erp': application.student.erp if application.student else application.erp,
        'subject': application.subject,
        'message': application.message,
        'date': application.created_at.strftime('%d-%m-%Y'),
    }
    
    # Generate the PDF
    document_path = generate(application_data)
    return FileResponse(open(document_path, 'rb'), as_attachment=True)
    
    