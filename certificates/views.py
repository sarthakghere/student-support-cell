from django.shortcuts import render
from django.http import FileResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import formset_factory
from students.models import Student, Certificate
from .forms import FetchStudentForm, BonafideCertificateForm, BacklogForm,BacklogFormSet
from .certificate_generator import generate_bonafide_certificate

# Create your views here.
def is_authorized(user):
    return user.is_authenticated and (user.role == 'admin' or user.role == 'staff')


@login_required(login_url='authentication:login')
@user_passes_test(is_authorized, login_url='authentication:login')
def certificates(request):
    return render(request, 'certificates/certificates_home.html')


BacklogFormSet = formset_factory(BacklogForm, extra=1)  # Ensure it allows dynamic additions

@login_required(login_url='authentication:login')
@user_passes_test(is_authorized, login_url='authentication:login')
def bonafide_certificate(request):
    fetch_student_form = FetchStudentForm()
    bonafide_form = None
    backlog_formset = BacklogFormSet()  # Always initialize the formset
    student_data = None
    has_backlogs = None  

    if request.method == "POST":
        if "fetch_details" in request.POST: 
            fetch_student_form = FetchStudentForm(request.POST)
            if fetch_student_form.is_valid():
                prn = fetch_student_form.cleaned_data["PRN"]
                student = Student.objects.filter(prn=prn).first()
                if Certificate.objects.filter(issued_to=student, certificate_type=Certificate.CertificateTypes.BC).exists():
                    fetch_student_form.add_error("PRN", "Bonafide Certificate already issued for this student.")
                if student:
                    student_data = {
                        "PRN": student.prn,
                        "first_name": student.user.first_name,
                        "last_name": student.user.last_name,
                        "gender": student.gender,
                        "fathers_name": "",
                        "course": student.program,
                        "course_start": student.course_start_year,
                        "course_end": student.course_start_year + student.course_duration,  
                    }
                    bonafide_form = BonafideCertificateForm(initial=student_data)
                else:
                    fetch_student_form.add_error("PRN", "No student found with this PRN.")

        elif "confirm_backlogs" in request.POST:  
            has_backlogs = request.POST.get("has_backlogs") == "yes"
            bonafide_form = BonafideCertificateForm(request.POST)
            backlog_formset = BacklogFormSet(request.POST if has_backlogs else None)

        elif "generate_certificate" in request.POST:
            bonafide_form = BonafideCertificateForm(request.POST)
            has_backlogs = request.POST.get("has_backlogs") == "yes"
            
            backlog_data = []
            if has_backlogs and request.POST.get("backlog_data"):
                import json
                backlog_data = json.loads(request.POST.get("backlog_data"))

            if bonafide_form.is_valid():
                student_data = bonafide_form.cleaned_data
                certificate_path = generate_bonafide_certificate(student_data, backlog_data)

                if certificate_path:
                    certificate = Certificate.objects.create(
                        issued_to=Student.objects.get(prn=student_data["PRN"]),
                        certificate_type=Certificate.CertificateTypes.BC,
                        file_path=certificate_path,
                        issued_by=request.user,
                        details = f"Bonafide Certificate for {student_data['first_name']} {student_data['last_name']} PRN: {student_data['PRN']}"
                    )
                    certificate.save()
                    return FileResponse(open(certificate_path, "rb"), as_attachment=True)

    return render(request, "certificates/bonafide_certificate.html", {
        "fetch_student_form": fetch_student_form,
        "bonafide_form": bonafide_form,
        "backlog_formset": backlog_formset,  
        "student_data": student_data,
        "has_backlogs": has_backlogs,
    })
