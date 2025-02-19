from django import forms
from .models import User

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')

    USERNAME_FIELD = 'email'  # Use email as the login field
    REQUIRED_FIELDS = []  

class StaffForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True, label='First Name')
    middle_name = forms.CharField(max_length=100, required=False, label='Middle Name')
    last_name = forms.CharField(max_length=100, required=True, label='Last Name')
    email = forms.EmailField(max_length=100, required=True, label='Email')
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Confirm Password')

    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = instance

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.instance.id if self.instance else None).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data

class StaffEditForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True, label='First Name')
    middle_name = forms.CharField(max_length=100, required=False, label='Middle Name')
    last_name = forms.CharField(max_length=100, required=True, label='Last Name')
    email = forms.EmailField(max_length=100, required=True, label='Email')
