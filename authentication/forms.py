from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')

    USERNAME_FIELD = 'email'  # Use email as the login field
    REQUIRED_FIELDS = []  

class StaffForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True, label='First Name')
    last_name = forms.CharField(max_length=100, required=True, label='Last Name')
    email = forms.EmailField(max_length=100, required=True, label='Email')
    password = forms.PasswordInput()
    confirm_password = forms.PasswordInput()
    