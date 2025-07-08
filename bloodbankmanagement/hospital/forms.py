from django import forms
from django.contrib.auth.models import User
from . import models
from hospital import models


class HospitalUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']  
        widgets = {
            'password': forms.PasswordInput()}

class HospitalForm(forms.ModelForm):
    class Meta:
        model = models.Hospital  # Use the Hospital model instead of Patient
        fields = ['hospital_name', 'registration_number', 'contact_person', 'address', 'mobile', 'profile_pic']