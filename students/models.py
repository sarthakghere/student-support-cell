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

    class CategoryChoices(models.TextChoices):
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
    erp = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, validators=[phone_regex])
    dob = models.DateField()
    gender = models.CharField(max_length=5, default=None, null= True, choices=GenderChoices.choices)
    alternate_phone_number = models.CharField(max_length=15, validators=[phone_regex], blank=True, null=True)
    fathers_name = models.CharField(max_length=50)
    fathers_contact = models.CharField(max_length=15, validators=[phone_regex])
    mothers_name = models.CharField(max_length=50)
    mothers_contact = models.CharField(max_length=15, validators=[phone_regex])

    category = models.CharField(max_length=20, choices=CategoryChoices.choices, default=CategoryChoices.GEN)
    disability = models.BooleanField(default=False)

    # Need Additionally In Excel Sheet
    program = models.CharField(max_length=50, choices=ProgramChoices.choices)
    semester = models.CharField(max_length=10, choices=SemesterChoices.choices, default=SemesterChoices.SEM1)
    course_start_year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(date.today().year)])
    course_duration = models.IntegerField(choices=CourseDurationChoices.choices)
    
    abc_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    permament_address = models.TextField()
    current_address = models.TextField()
    state = models.CharField(max_length=50)

    # Optional Fields
    cet_rank = models.IntegerField(null=True, blank=True)
    special_quota = models.CharField(max_length=50, null=True, blank=True)
    family_income = models.FloatField(null=True, blank=True)
    previous_academic_stream = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['user__full_name']


class Certificate(models.Model):

    class CertificateTypes(models.TextChoices):
        TC = "TC", "Transfer Certificate"
        CC = "CC", "Character Certificate"
        BC = "BC", "Bonafide Certificate"

    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    class IsDuplicate(models.TextChoices):
        YES = "Y", "Yes"
        NO = "N", "No"
    
    certificate_type = models.CharField(max_length=2, choices=CertificateTypes.choices)
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
    is_duplicate = models.CharField(max_length=1, choices=IsDuplicate.choices, default=IsDuplicate.NO)
    approval_status = models.CharField(max_length=10, choices=StatusChoices.choices)  # Default for originals
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_certificates')
    requested_on = models.DateTimeField(auto_now_add=True)
    approved_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_certificate_type_display()} for {self.issued_to.user.first_name} {self.issued_to.user.last_name}"

    class Meta:
        ordering = ['-issue_date']

