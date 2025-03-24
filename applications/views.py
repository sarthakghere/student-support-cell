from django.shortcuts import render, redirect
from .models import StudentApplication
from .generate_application import generate
from django.http import FileResponse
from django.db.models import Q
import os

def applications_home(request):
    return render(request, 'applications/applications_home.html')

def list_applications(request):
    search_query = request.GET.get('search', '').strip()
    applications = StudentApplication.objects.filter(is_archived=False)

    if search_query:
        applications = applications.filter(is_archived=False).filter(
            Q(application_type__iexact=search_query) |  # Exact match for application_type
            Q(prn__icontains=search_query) |
            Q(erp__icontains=search_query) |  # Added ERP search
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    return render(request, 'applications/list_applications.html', {'applications': applications})

def list_archived_applications(request):
    search_query = request.GET.get('search', '').strip()
    applications = StudentApplication.objects.filter(is_archived=True)
    if search_query:
        applications = applications.filter(
            Q(application_type__iexact=search_query) |  # Exact match for application_type
            Q(prn__icontains=search_query) |
            Q(erp__icontains=search_query) |  # Added ERP search
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    return render(request, 'applications/list_archived_applications.html', {'applications': applications})

def archive_application(request, pk):
    application = StudentApplication.objects.get(pk=pk)
    application.is_archived = True
    application.save()
    return redirect('applications:list_applications')

def unarchive_application(request, pk):
    application = StudentApplication.objects.get(pk=pk)
    application.is_archived = False
    application.save()
    return redirect('applications:list_archived_applications')


def view_application(request, pk):
    application = StudentApplication.objects.get(pk=pk)
    if application.application_type == StudentApplication.ApplicationTypesChoices.GENERAL:
        return render(request, 'applications/view_general_application.html', {'application': application})
    if application.application_type == StudentApplication.ApplicationTypesChoices.CERTIFICATE_ISSUE_REQUEST:
        return render(request, 'applications/view_certificate_request.html', {'application': application})

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
    
    