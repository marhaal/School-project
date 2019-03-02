from django import forms
from .models import Post, Comment, Loan, Comment2, Community
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RequestsForm(forms.ModelForm):

    community = forms.ModelChoiceField(queryset=Community.objects.all().order_by('name'))

    class Meta:
        model = Post
        fields=('title', 'text', 'community')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    age = forms.CharField(required=True)
    gender = forms.CharField(required=True)
    gender = forms.ChoiceField(choices=[('kvinne', 'Kvinne'), ('mann', 'Mann')])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'gender', 'age')


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'gender', 'age')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class CommentForm2(forms.ModelForm):

    class Meta:
        model = Comment2
        fields = ('author', 'text',)

class LoansForm(forms.ModelForm):
    community = forms.ModelChoiceField(queryset=Community.objects.all().order_by('name'), to_field_name='name')
    class Meta:
        model = Loan
        fields=('title', 'text', 'community',)


class CommunityForm(forms.ModelForm):

    class Meta:
        model = Community
        fields = ('name', 'text', 'address', 'longitude', 'latitude',)

class PickCommunityForm(forms.ModelForm):
    community = forms.ModelChoiceField(queryset=Community.objects.all().order_by('name'), to_field_name='name')
    class Meta:
        model = Community
        fields=('community',)
