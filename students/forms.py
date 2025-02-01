from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from datetime import date
from .models import Student  # Assuming Student model contains the choices

class StudentForm(forms.Form):
    prn = forms.CharField(
        max_length=20,
        required=True,
        label="PRN"
    )
    email = forms.EmailField(
        required=True,
        label="Email Address"
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        label="First Name"
    )
    middle_name = forms.CharField(
        max_length=100,
        required=False,
        label="Middle Name"
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        label="Last Name"
    )
    dob = forms.DateField(
        required=True,
        label="Date of Birth",
        widget=forms.SelectDateWidget(years=range(1970, date.today().year + 1))
    )
    phone_number = forms.CharField(label="Phone Number")
    gender = forms.ChoiceField(
        choices=Student.GenderChoices.choices,
        required=False,
        label="Gender"
    )
    program = forms.ChoiceField(
        choices=Student.ProgramChoices.choices,
        required=True,
        label="Program"
    )
    semester = forms.ChoiceField(
        choices=Student.SemesterChoices.choices,
        required=True,
        label="Semester"
    )
    course_start_year = forms.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(date.today().year)],
        required=True,
        label="Course Start Year"
    )
    course_duration = forms.ChoiceField(
        choices=Student.CourseDurationChoices.choices,
        required=True,
        label="Course Duration"
    )
    caste = forms.ChoiceField(
        choices=Student.CasteChoices.choices,
        required=True,
        label="Caste"
    )
    religion = forms.CharField(
        max_length=100,
        required=True,
        label="Religion"
    )
    nationality = forms.CharField(
        max_length=100,
        required=True,
        label="Nationality"
    )
    pan = forms.CharField(
        max_length=10,
        label="PAN",
        validators=[RegexValidator(
            regex=r'^[A-Z]{5}\d{4}[A-Z]{1}$',
            message="PAN must follow the format: 5 letters, 4 digits, 1 letter (e.g., ABCDE1234F)."
        )],
        required=False
    )
    aadhar = forms.CharField(
        max_length=12,
        label="Aadhar Number",
        validators=[RegexValidator(
            regex=r'^\d{12}$',
            message="Aadhar must be exactly 12 digits."
        )],
        required=False
    )
    abc_id = forms.CharField(
        max_length=20,
        label="ABC ID",
        required=False
    )
    street_address = forms.CharField(
        widget=forms.TextInput,
        required=True,
        label="Street Address"
    )
    city = forms.CharField(
        max_length=50,
        required=True,
        label="City"
    )
    state = forms.CharField(
        max_length=50,
        required=True,
        label="State"
    )
    pincode = forms.CharField(
        max_length=6,
        required=True,
        label="Pincode",
        validators=[RegexValidator(
            regex=r'^\d{6}$',
            message="Pincode must be exactly 6 digits."
        )]
    )
    country = forms.CharField(
        max_length=50,
        required=True,
        label="Country"
    )

class EditStudentForm(forms.Form):
    prn = forms.CharField(max_length=20, required=True, label="PRN")
    email = forms.EmailField(required=True, label="Email Address")

    first_name = forms.CharField(max_length=100, required=True, label="First Name")
    middle_name = forms.CharField(max_length=100, required=False, label="Middle Name")
    last_name = forms.CharField(max_length=100,required=True, label="Last Name")

    dob = forms.DateField(required=True, label="Date of Birth", widget=forms.SelectDateWidget(years=range(1970, date.today().year + 1)))
    phone_number = forms.CharField(label="Phone Number")
    gender = forms.ChoiceField(choices=Student.GenderChoices.choices, required=False, label="Gender")
    caste = forms.ChoiceField(choices=Student.CasteChoices.choices, required=True, label="Caste")
    religion = forms.CharField(max_length=100, required=True, label="Religion")
    nationality = forms.CharField(max_length=100, required=True, label="Nationality")

    program = forms.ChoiceField(choices=Student.ProgramChoices.choices, required=True, label="Program")
    semester = forms.ChoiceField(choices=Student.SemesterChoices.choices, required=True, label="Semester")

    pan = forms.CharField(max_length=10, label="PAN", validators=[RegexValidator(regex=r'^[A-Z]{5}\d{4}[A-Z]{1}$', message="PAN must follow the format: 5 letters, 4 digits, 1 letter (e.g., ABCDE1234F).")], required=False)
    aadhar = forms.CharField(max_length=12, label="Aadhar Number", validators=[RegexValidator(regex=r'^\d{12}$', message="Aadhar must be exactly 12 digits.")], required=False)
    abc_id = forms.CharField(max_length=20, label="ABC ID", required=False)

    street_address = forms.CharField(widget=forms.TextInput, required=True, label="Street Address")
    city = forms.CharField(max_length=50, required=True, label="City")
    state = forms.CharField(max_length=50, required=True, label="State")
    pincode = forms.CharField(max_length=6, required=True, label="Pincode", validators=[RegexValidator(regex=r'^\d{6}$', message="Pincode must be exactly 6 digits.")])
    country = forms.CharField(max_length=50, required=True, label="Country")

    def __init__(self, *args, **kwargs):
        super(EditStudentForm, self).__init__(*args, **kwargs)
        self.fields['prn'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['pan'].widget.attrs['readonly'] = True
        self.fields['aadhar'].widget.attrs['readonly'] = True
        self.fields['abc_id'].widget.attrs['readonly'] = True