from django import forms
from users.models import Member

class PostCreationForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.TextInput)
    