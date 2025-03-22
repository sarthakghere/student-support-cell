from django.db import models
from students.models import Student, Certificate
from authentication.models import User

# Create your models here.
class StudentApplication(models.Model):

    class StatusChoices(models.TextChoices):
        PENDING = 'Pending'
        RESOLVED = 'Resolved'

    prn = models.CharField(max_length=100)
    erp = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications', null=True, blank=True)
    application_type = models.CharField(max_length=100, null=False, blank=False)
    subject = models.CharField(max_length=256, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    certificate_type = models.CharField(max_length=100, null=True, blank=True, choices=Certificate.CertificateTypes.choices)
    status = models.CharField(max_length=100, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    managed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='managed_applications', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        if self.student:
            return 'Application by ' + self.student.prn
        else:
            return 'Application by ' + self.prn