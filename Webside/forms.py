from django import forms
from .models import Post, Comment, Loan, Comment2, Community
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RequestsForm(forms.ModelForm):

    community = forms.ModelChoiceField(queryset=Community.objects.all().order_by('name'))

    class Meta:
        model = Post
        fields=('title', 'text', 'community')
        labels = {'title': "Tittel", 'text': 'Tekst'}


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    age = forms.CharField(required=True)
    gender = forms.CharField(required=True)
    gender = forms.ChoiceField(choices=[('kvinne', 'Kvinne'), ('mann', 'Mann'), ('annet', 'Annet')])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'gender', 'age')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
        labels = {'author': "Navn", 'text': 'Tekst'}

class CommentForm2(forms.ModelForm):

    class Meta:
        model = Comment2
        fields = ('author', 'text',)
        labels = {'author': "Navn", 'text': 'Tekst'}

class LoansForm(forms.ModelForm):
    community = forms.ModelChoiceField(queryset=Community.objects.all().order_by('name'), to_field_name='name')
    class Meta:
        model = Loan
        fields=('title', 'text', 'community')
        labels = {'title': "Tittel", 'text': 'Tekst'}


class CommunityForm(forms.ModelForm):

    class Meta:
        model = Community
        fields = ('name', 'text', 'address', 'longitude', 'latitude',)
        labels = {'name': "Navn", 'text': "Beskrivelse", 'address': "Adresse", 'longitude': "Lengegrad", 'latitude': "Breddegrad"}
