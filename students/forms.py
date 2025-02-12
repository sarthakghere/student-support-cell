from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from datetime import date
from .models import Student  # Assuming Student model contains the choices

class StudentForm(forms.Form):
    prn = forms.CharField(max_length=20,required=True,label="PRN")
    erp = forms.CharField(max_length=20,required=True,label="ERP ID")
    email = forms.EmailField(required=True,label="Email Address")
    abc_id = forms.CharField(max_length=20,label="ABC ID",required=False)
    full_name = forms.CharField(max_length=100,required=True,label="Full Name")
    dob = forms.DateField(required=True, label="Date of Birth", widget=forms.SelectDateWidget(years=range(date.today().year, 1970, -1)))
    gender = forms.ChoiceField(choices=Student.GenderChoices.choices,required=False,label="Gender")
    
    phone_number = forms.CharField(label="Phone Number", validators=[Student.phone_regex], required=True, max_length=10)
    alternate_phone_number = forms.CharField(label="Alternate Phone Number", validators=[Student.phone_regex], required=False, max_length=10)
    fathers_name = forms.CharField(max_length=50, required=True, label="Father's Name")
    fathers_contact = forms.CharField(label="Father's Contact", validators=[Student.phone_regex], required=False, max_length=10)
    mothers_name = forms.CharField(max_length=50, required=True, label="Mother's Name")
    mothers_contact = forms.CharField(label="Mother's Contact", validators=[Student.phone_regex], required=False, max_length=10)

    program = forms.ChoiceField(choices=Student.ProgramChoices.choices,required=True,label="Program")
    semester = forms.ChoiceField(choices=Student.SemesterChoices.choices,required=True,label="Semester")
    course_start_year = forms.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(date.today().year)],required=True,label="Course Start Year")
    course_duration = forms.ChoiceField(choices=Student.CourseDurationChoices.choices,required=True,label="Course Duration", help_text="In years")

    permanent_address = forms.CharField(widget=forms.TextInput,required=True,label="Permanent Address")
    current_address = forms.CharField(widget=forms.TextInput,required=True,label="Current Address")
    state = forms.CharField(max_length=50,required=True,label="State")

    category = forms.ChoiceField(choices=Student.CategoryChoices.choices,required=True,label="Category")
    disability = forms.BooleanField(required=False,label="Disability")
    cet_rank = forms.IntegerField(required=False,label="CET Rank")
    special_quota = forms.CharField(max_length=50,required=False,label="Special Quota")
    family_income = forms.FloatField(required=False,label="Family Income")
    previous_academic_stream = forms.CharField(max_length=50,required=False,label="Previous Academic Stream")



class EditStudentForm(StudentForm):

    def __init__(self, *args, **kwargs):
        super(EditStudentForm, self).__init__(*args, **kwargs)
        self.fields['prn'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['abc_id'].widget.attrs['readonly'] = True
        self.fields['cet_rank'].widget.attrs['readonly'] = True

class ExcelInputForm(forms.Form):
    excel_file = forms.FileField(required=True, label= "Upload Excel File")
    sheet_name = forms.CharField(max_length=255, required=True)
    program = forms.ChoiceField(choices=Student.ProgramChoices.choices, required=True)
    semester = forms.ChoiceField(choices=Student.SemesterChoices.choices, required=True)
    course_start_year = forms.IntegerField(required=True)
    course_duration = forms.ChoiceField(choices=Student.CourseDurationChoices.choices, required=True)