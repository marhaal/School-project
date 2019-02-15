from django import forms
from .models import Post

class RequestsForm(forms.ModelForm):

    class Meta:
        model = Post
        fields=('title', 'text',)
