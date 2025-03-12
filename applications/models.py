from django.db import models
from students.models import Student

# Create your models here.
class StudentApplication(models.Model):
    prn = models.CharField(max_length=100)
    erp = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=256)
    message = models.TextField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        if self.student:
            return 'Application by ' + self.student.prn
        else:
            return 'Application by ' + self.prn