from django import forms
from OG.models import *

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password','email']
        help_texts={'username':''}
        widgets={'password':forms.PasswordInput}

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['address','profile_pic']

