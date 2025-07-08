from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from blood import forms as bforms
from blood import models as bmodels


from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from hospital import forms

from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from hospital import forms

def hospital_signup_view(request):
    userForm=forms.HospitalUserForm()
    hospitalForm=forms.HospitalForm()
    mydict={'userForm':userForm,'hospitalForm':hospitalForm}
    if request.method=='POST':
        userForm=forms.HospitalUserForm(request.POST)
        hospitalForm=forms.HospitalForm(request.POST,request.FILES)
        if userForm.is_valid() and hospitalForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            hospital=hospitalForm.save(commit=False)
            hospital.user=user
            #hospital.blood_group=hospitalForm.cleaned_data['blood_group'] 
            hospital.save()
            my_hospital_group = Group.objects.get_or_create(name='Hospital')
            my_hospital_group[0].user_set.add(user)
        return  redirect('hospitallogin')
    return render(request,'hospital/hospitalsignup.html',context=mydict)

def hospital_dashboard_view(request):
    hospital= models.Hospital.objects.get(user_id=request.user.id)
    dict={
        'requestpending': bmodels.BloodRequest.objects.all().filter(request_by_hospital=hospital).filter(status='Pending').count(),
        'requestapproved': bmodels.BloodRequest.objects.all().filter(request_by_hospital=hospital).filter(status='Approved').count(),
        'requestmade': bmodels.BloodRequest.objects.all().filter(request_by_hospital=hospital).count(),
        'requestrejected': bmodels.BloodRequest.objects.all().filter(request_by_hospital=hospital).filter(status='Rejected').count(),
       

    }
   
    dict['requests'] = bmodels.BloodRequest.objects.filter(request_by_hospital=hospital)

    return render(request,'hospital/hospital_dashboard.html',context=dict)

@login_required(login_url='hospitallogin')
def make_request_view(request):
    request_form = bforms.RequestForm()
    if request.method == 'POST':
        request_form = bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_group = request_form.cleaned_data['blood_group']
            unit = request_form.cleaned_data['unit']
            hospital = models.Hospital.objects.get(user_id=request.user.id)

            # Always create request with status "Pending"
            bmodels.BloodRequest.objects.create(
                blood_group=blood_group,
                unit=unit,
                request_by_hospital=hospital,
                status='Pending'   # ✅ Always pending initially
            )

            return redirect('my-request')

    return render(request, 'hospital/makerequest.html', {'request_form': request_form})


def my_request_view(request):
    hospital= models.Hospital.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_hospital=hospital)
    return render(request,'hospital/my_request.html',{'blood_request':blood_request})


