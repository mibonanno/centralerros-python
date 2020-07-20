from django import forms

from api.models import User

class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
