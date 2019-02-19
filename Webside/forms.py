from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RequestsForm(forms.ModelForm):

    class Meta:
        model = Post
        fields=('title', 'text',)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    GENDERS = ((1, "Mann"), (2, "Kvinne"))
    gender = forms.CharField(required=True)
    age = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'gender', 'age', 'password1', 'password2', )
