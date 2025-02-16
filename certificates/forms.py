from django import forms
from students.models import Student

class FetchStudentForm(forms.Form):
    PRN = forms.CharField(label='PRN', max_length=100, help_text='Enter the PRN of the student', required=True)

class BonafideCertificateForm(forms.Form):
    PRN = forms.CharField(label='PRN', max_length=100, required=True)
    full_name = forms.CharField(label='Full Name', max_length=100, required=True)
    gender = forms.ChoiceField(label='Gender', choices=Student.GenderChoices.choices, required=True)
    fathers_name = forms.CharField(label='Father\'s Name', max_length=100, required=True)
    course = forms.CharField(label='Course', max_length=100, required=True)
    course_start = forms.IntegerField(label='Course Start', required=True)
    course_end = forms.IntegerField(label='Course End', required=True)

class BacklogForm(forms.Form):
    subject_name = forms.CharField(max_length=255, label="Subject Name")
    declared_fail = forms.CharField(max_length=100, label="Declared Failed")
    declared_pass = forms.CharField(max_length=100, label="Declared Pass")

BacklogFormSet = forms.formset_factory(BacklogForm, extra=1)