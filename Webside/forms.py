from django import forms
from .models import *
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
    age = forms.IntegerField(max_value=150, min_value=0, required=True)
    gender = forms.CharField(required=True)
    gender = forms.ChoiceField(choices=[('kvinne', 'Kvinne'), ('mann', 'Mann'), ('annet', 'Annet')])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'gender', 'age')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': 'Tekst'}

class CommentForm2(forms.ModelForm):

    class Meta:
        model = Comment2
        fields = ('text',)
        labels = {'text': 'Tekst'}

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
        labels = {'name': "Navn", 'text': "Beskrivelse", 'address': "Adresse", 'longitude': "Lengdegrad", 'latitude': "Breddegrad"}

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('reason',)
        labels = {'reason': "",}


class ContactForm(forms.ModelForm):
    issue_alternative = forms.ChoiceField(choices=[('spørsmål', 'Har du noen spørsmål?'), ('feil på nettsiden', 'Er det noe som ikke fungerer på nettsiden?'), ('annet', 'Annet')])
    issue_text = forms.CharField(required=True, max_length=254)

    class Meta:
        model = Contact
        fields = ('issue_alternative', 'issue_text')
        labels = {'issue_alternative': "Velg et alternativ", 'issue_text': "Tekst"}

class ProfileUpdateForm(forms.ModelForm):
    YEARS= [x for x in range(1900,2021)]
    birth_date = forms.DateField( initial="1995-06-03", widget=forms.SelectDateWidget(years=YEARS))
    class Meta:
        model = Profile
        fields = ('bio','birth_date','location','image')
        labels = {'bio': "Bio", 'birth_date': "Fødselsdato", 'location': "Lokasjon", 'image' : "Profilbilde"}
