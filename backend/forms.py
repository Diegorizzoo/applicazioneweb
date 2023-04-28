from django import forms
from .models import QA
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class QAForm(forms.ModelForm):
    class Meta:
        model = QA
        fields = ['question', 'answer']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email/Codice fiscale", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    codice_fiscale = forms.CharField(max_length=16, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'codice_fiscale', 'password1', 'password2')




