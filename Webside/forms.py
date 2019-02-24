from django import forms
from .models import Post, Comment, Loan
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RequestsForm(forms.ModelForm):

    class Meta:
        model = Post
        fields=('title', 'text',)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    gender = forms.CharField(required=True)
    age = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'gender', 'age')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class LoansForm(forms.ModelForm):

    class Meta:
        model = Loan
        fields=('text',)
