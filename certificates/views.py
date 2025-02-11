from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from django.contrib import messages
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import formset_factory
from students.models import Student, Certificate
from .forms import FetchStudentForm, BonafideCertificateForm, BacklogForm,BacklogFormSet
from .certificate_generator import generate_bonafide_certificate
import json

# Create your views here.
def is_authorized(user):
    return user.is_authenticated and (user.role == 'admin' or user.role == 'staff')

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'


@login_required(login_url='authentication:login')
@user_passes_test(is_authorized, login_url='authentication:login')
def certificates(request):
    return render(request, 'certificates/certificates_home.html')


BacklogFormSet = formset_factory(BacklogForm, extra=1)  # Ensure it allows dynamic additions

def is_certificate_already_issued(student):
    return Certificate.objects.filter(
        issued_to=student, certificate_type=Certificate.CertificateTypes.BC
    ).exists()

def get_certificate_link(student):
    certificate_id = Certificate.objects.get(issued_to=student, certificate_type=Certificate.CertificateTypes.BC).id
    return f"/certificates/download-certificate/{certificate_id}/"


def get_student_initial_data(student: Student):
    # Prepare initial data from student instance for the BonafideCertificateForm.
    return {
        "PRN": student.prn,
        "full_name": student.user.full_name,
        "gender": student.gender,
        "fathers_name": student.fathers_name,
        "course": student.program,
        "course_start": student.course_start_year,
        "course_end": student.course_start_year + student.course_duration,
    }

@login_required(login_url='authentication:login')
@user_passes_test(is_authorized, login_url='authentication:login')
def download_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    return FileResponse(open(certificate.file_path, "rb"), as_attachment=True)

@login_required(login_url='authentication:login')
@user_passes_test(is_authorized, login_url='authentication:login')
def bonafide_certificate(request):
    fetch_student_form = FetchStudentForm()
    bonafide_form = None
    backlog_formset = BacklogFormSet()  # Always initialize the formset
    student_data = None
    has_backlogs = None  
    certificate = None

    # Handle Fetching Student Details
    if request.method == "POST" and "fetch_details" in request.POST:
        fetch_student_form = FetchStudentForm(request.POST)
        if fetch_student_form.is_valid():
            prn = fetch_student_form.cleaned_data["PRN"]
            student = Student.objects.filter(prn=prn).first()
            if student:
                if is_certificate_already_issued(student):
                    fetch_student_form.add_error("PRN", mark_safe(f"Bonafide Certificate already issued for this student. <a href='{get_certificate_link(student)}'>Click Here to download.</a>"))
                else:
                    student_data = get_student_initial_data(student)
                    bonafide_form = BonafideCertificateForm(initial=student_data)
            else:
                fetch_student_form.add_error("PRN", "No student found with this PRN.")

    # Handle Backlog Confirmation
    elif request.method == "POST" and "confirm_backlogs" in request.POST:
        has_backlogs = request.POST.get("has_backlogs") == "yes"
        bonafide_form = BonafideCertificateForm(request.POST)
        # Only bind the formset if there are backlogs
        backlog_formset = BacklogFormSet(request.POST if has_backlogs else None)

    # Handle Certificate Generation
    elif request.method == "POST" and "generate_certificate" in request.POST:
        bonafide_form = BonafideCertificateForm(request.POST)
        has_backlogs = request.POST.get("has_backlogs") == "yes"
        backlog_data = []
        backlog_json = request.POST.get("backlog_data")
        if has_backlogs and backlog_json:
            try:
                backlog_data = json.loads(backlog_json)
            except json.JSONDecodeError:
                messages.error(request, "Invalid backlog data format.")
                backlog_data = []

        if bonafide_form.is_valid():
            student_data = bonafide_form.cleaned_data
            bonafide_form = None
            student = get_object_or_404(Student, prn=student_data["PRN"])
            existing_certificate = Certificate.objects.filter(
                issued_to=student, certificate_type=Certificate.CertificateTypes.BC
            ).first()
            if existing_certificate:
                download_link = f"<a href='/certificates/download-certificate/{existing_certificate.id}/'>Click Here to download.</a>"
                messages.warning(request, mark_safe(f"Bonafide Certificate already exists. {download_link}"))
            else:
                certificate_path = generate_bonafide_certificate(student_data, backlog_data)
                if certificate_path:
                    certificate = Certificate.objects.create(
                        issued_to=student,
                        certificate_type=Certificate.CertificateTypes.BC,
                        file_path=certificate_path,
                        issued_by=request.user,
                        approval_status=Certificate.StatusChoices.APPROVED,
                        details=f"Bonafide Certificate for {student_data['full_name']} PRN: {student_data['PRN']}"
                    )
                    download_link = f"<a href='/certificates/download-certificate/{certificate.id}/'>Click Here to download.</a>"
                    messages.success(request, mark_safe(f"Bonafide Certificate generated successfully. {download_link}"))
                else:
                    messages.error(request, "Failed to generate certificate. Please try again.")

    context = {
        "fetch_student_form": fetch_student_form,
        "bonafide_form": bonafide_form,
        "backlog_formset": backlog_formset,
        "student_data": student_data,
        "has_backlogs": has_backlogs,
        "certificate": certificate,
    }
    return render(request, "certificates/bonafide_certificate.html", context)


@login_required(login_url='authentication:login')
@user_passes_test(is_authorized, login_url='authentication:login')
def approved_duplicate_certificate(request):
    search_query = request.GET.get('search', '').strip()
    
    # Filter certificates based on search query
    certificates = Certificate.objects.filter(is_duplicate=Certificate.IsDuplicate.YES)
    certificate = certificates.first()

    if search_query:
        certificates = certificates.filter(is_duplicate=Certificate.IsDuplicate.YES).filter(
            Q(certificate_type__icontains=search_query) |
            Q(issued_to__prn__icontains=search_query) |
            Q(issued_by__first_name__icontains=search_query) |
            Q(issued_by__last_name__icontains=search_query)
        )

    context = {
        "certificates": certificates,
    }
    return render(request, 'certificates/approved_duplicate_certificates.html', context)

@login_required(login_url='authentication:login')
@user_passes_test(is_admin, login_url='authentication:login')
def approve_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    certificate.approval_status = Certificate.StatusChoices.APPROVED
    certificate.save()
    messages.success(request, "Certificate approved successfully.")
    return redirect('authentication:approve_duplicate_certificates')

@login_required(login_url='authentication:login')
@user_passes_test(is_admin, login_url='authentication:login')
def reject_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    certificate.approval_status = Certificate.StatusChoices.REJECTED
    certificate.save()
    messages.success(request, "Certificate rejected.")
    return redirect('authentication:approve_duplicate_certificates')