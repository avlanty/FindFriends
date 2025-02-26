from .models import Member
from django import forms

class MemberRegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta: 
        model = Member
        fields = ['first_name', 'last_name', 'username', 'email', 'password'] 

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Member.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    

class MemberLoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)




