from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from authentication.models import User
from datetime import date

class Student(models.Model):
    pincode_regex = RegexValidator(
    regex=r'^\d{6}$',
    message="Pincode must be exactly 6 digits."
)

    phone_regex = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be exactly 10 digits."
)

    class ProgramChoices(models.TextChoices):
        BCA = "BCA", "Bachelor of Computer Applications"
        BBA = "BBA", "Bachelor of Business Administration"
        MBA = "MBA", "Master of Business Administration"
        BBA_LLB = "BBA LLB", "Bachelor of Business Administration and Bachelor of Legislative Law"
        LLB = "LLB", "Bachelor of Legislative Law"

    class SemesterChoices(models.TextChoices):
        SEM1 = "1", "Semester 1"
        SEM2 = "2", "Semester 2"
        SEM3 = "3", "Semester 3"
        SEM4 = "4", "Semester 4"
        SEM5 = "5", "Semester 5"
        SEM6 = "6", "Semester 6"
        SEM7 = "7", "Semester 7"
        SEM8 = "8", "Semester 8"

    class GenderChoices(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    class CasteChoices(models.TextChoices):
        GEN = "GEN", "General"
        OBC = "OBC", "Other Backward Class"
        SC = "SC", "Scheduled Caste"
        ST = "ST", "Scheduled Tribe"

    class CourseDurationChoices(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    prn = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, validators=[phone_regex])
    dob = models.DateField()
    gender = models.CharField(max_length=5, default=None, null= True, choices=GenderChoices.choices)
    program = models.CharField(max_length=50, choices=ProgramChoices.choices)
    semester = models.CharField(max_length=10, choices=SemesterChoices.choices, default=SemesterChoices.SEM1)
    course_start_year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(date.today().year)])
    course_duration = models.IntegerField(choices=CourseDurationChoices.choices)
    caste = models.CharField(max_length=20, choices=CasteChoices.choices, default=CasteChoices.GEN)
    religion = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    pan = models.CharField(
        max_length=10, 
        unique=True, 
        null=True, 
        blank=True,
        validators=[RegexValidator(
            regex=r'^[A-Z]{5}\d{4}[A-Z]{1}$',
            message="PAN must follow the format: 5 letters, 4 digits, 1 letter (e.g., ABCDE1234F)."
        )]
    )
    aadhar = models.CharField(
        max_length=12, 
        unique=True, 
        null=True, 
        blank=True,
        validators=[RegexValidator(
            regex=r'^\d{12}$',
            message="Aadhar must be exactly 12 digits."
        )]
    )
    abc_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    street_address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6, validators=[pincode_regex])
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['user__first_name', 'user__last_name']


class Certificate(models.Model):
    CERTIFICATE_TYPES = (
        ('TC', 'Transfer Certificate'),
        ('CC', 'Character Certificate'),
        ('BC', 'Bonafide Certificate'),
    )
    certificate_type = models.CharField(max_length=2, choices=CERTIFICATE_TYPES)
    issued_to = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='certificates'
    )
    issued_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='issued_certificates'
    )
    issue_date = models.DateField(default=date.today)
    details = models.TextField(blank=True, null=True)
    file_path = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
    )

    def __str__(self):
        return f"{self.get_certificate_type_display()} for {self.issued_to.first_name} {self.issued_to.last_name}"

    class Meta:
        ordering = ['-issue_date']

