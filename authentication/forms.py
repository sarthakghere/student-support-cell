from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')

    USERNAME_FIELD = 'email'  # Use email as the login field
    REQUIRED_FIELDS = []  