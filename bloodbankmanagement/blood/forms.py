from django import forms

from . import models
from donor.models import BloodDonate


class BloodForm(forms.ModelForm):
    class Meta:
        model=models.Stock
        fields=['blood_group','unit']

class RequestForm(forms.ModelForm):
    class Meta:
        model=models.BloodRequest
        fields=['reason','blood_group','unit']
class BloodDonateApprovalForm(forms.ModelForm):
    class Meta:
        model = BloodDonate
        fields = ['status', 'appointment_date', 'appointment_time', 'location']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter donation location'}),
        }
from django import forms
from .models import DonationCamp

class DonationCampForm(forms.ModelForm):
    class Meta:
        model = DonationCamp
        fields = '__all__'
