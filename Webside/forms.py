from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RequestsForm(forms.ModelForm):

    class Meta:
        model = Post
        fields=('title', 'text',)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Kreves. Skriv inn en gyldig emailadresse.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )