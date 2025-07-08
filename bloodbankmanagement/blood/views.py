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
from donor import models as dmodels
from hospital import models as pmodels
from donor import forms as dforms
from hospital import forms as pforms
from blood.forms import BloodDonateApprovalForm
from django.shortcuts import get_object_or_404
from donor.models import BloodDonate 
from .models import Stock 
from django.utils import timezone
from django.contrib import messages
from blood.models import BloodRequest, Stock
import blood.models as bmodels
from django.shortcuts import render, redirect
from .forms import DonationCampForm
from .models import DonationCamp
from django.contrib.auth.decorators import login_required


def home_view(request):
    x=models.Stock.objects.all()
    print(x)
    if len(x)==0:
        blood1=models.Stock()
        blood1.blood_group="A+"
        blood1.save()

        blood2=models.Stock()
        blood2.blood_group="A-"
        blood2.save()

        blood3=models.Stock()
        blood3.blood_group="B+"
        blood3.save()        

        blood4=models.Stock()
        blood4.blood_group="B-"
        blood4.save()

        blood5=models.Stock()
        blood5.blood_group="AB+"
        blood5.save()

        blood6=models.Stock()
        blood6.blood_group="AB-"
        blood6.save()

        blood7=models.Stock()
        blood7.blood_group="O+"
        blood7.save()

        blood8=models.Stock()
        blood8.blood_group="O-"
        blood8.save()

    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'blood/index.html')

def is_donor(user):
    return user.groups.filter(name='DONOR').exists()

def is_hospital(user):
    return user.groups.filter(name='Hospital').exists()


def afterlogin_view(request):
    if is_donor(request.user):      
        return redirect('donor-dashboard')
                
    elif is_hospital(request.user):
        return redirect('hospitals-dashboard')
    else:
        return redirect('admin-dashboard')

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    totalunit=models.Stock.objects.aggregate(Sum('unit'))
    dict={

        'A1':models.Stock.objects.get(blood_group="A+"),
        'A2':models.Stock.objects.get(blood_group="A-"),
        'B1':models.Stock.objects.get(blood_group="B+"),
        'B2':models.Stock.objects.get(blood_group="B-"),
        'AB1':models.Stock.objects.get(blood_group="AB+"),
        'AB2':models.Stock.objects.get(blood_group="AB-"),
        'O1':models.Stock.objects.get(blood_group="O+"),
        'O2':models.Stock.objects.get(blood_group="O-"),
        'totaldonors':dmodels.Donor.objects.all().count(),
        'totalbloodunit':totalunit['unit__sum'],
        'totalrequest':models.BloodRequest.objects.all().count(),
        'totalapprovedrequest':models.BloodRequest.objects.all().filter(status='Approved').count()
    }
    return render(request,'blood/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_blood_view(request):
    dict={
        'bloodForm':forms.BloodForm(),
        'A1':models.Stock.objects.get(blood_group="A+"),
        'A2':models.Stock.objects.get(blood_group="A-"),
        'B1':models.Stock.objects.get(blood_group="B+"),
        'B2':models.Stock.objects.get(blood_group="B-"),
        'AB1':models.Stock.objects.get(blood_group="AB+"),
        'AB2':models.Stock.objects.get(blood_group="AB-"),
        'O1':models.Stock.objects.get(blood_group="O+"),
        'O2':models.Stock.objects.get(blood_group="O-"),
    }
    if request.method=='POST':
        bloodForm=forms.BloodForm(request.POST)
        if bloodForm.is_valid() :        
            blood_group=bloodForm.cleaned_data['blood_group']
            stock=models.Stock.objects.get(blood_group=blood_group)
            stock.unit=bloodForm.cleaned_data['unit']
            stock.save()
        return HttpResponseRedirect('admin-blood')
    return render(request,'blood/admin_blood.html',context=dict)


@login_required(login_url='adminlogin')
def admin_donor_view(request):
    donors=dmodels.Donor.objects.all()
    return render(request,'blood/admin_donor.html',{'donors':donors})

@login_required(login_url='adminlogin')
def update_donor_view(request,pk):
    donor=dmodels.Donor.objects.get(id=pk)
    user=dmodels.User.objects.get(id=donor.user_id)
    userForm=dforms.DonorUserForm(instance=user)
    donorForm=dforms.DonorForm(request.FILES,instance=donor)
    mydict={'userForm':userForm,'donorForm':donorForm}
    if request.method=='POST':
        userForm=dforms.DonorUserForm(request.POST,instance=user)
        donorForm=dforms.DonorForm(request.POST,request.FILES,instance=donor)
        if userForm.is_valid() and donorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor=donorForm.save(commit=False)
            donor.user=user
            donor.blood_group=donorForm.cleaned_data['blood_group']
            donor.save()
            return redirect('admin-donor')
    return render(request,'blood/update_donor.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_donor_view(request,pk):
    donor=dmodels.Donor.objects.get(id=pk)
    user=User.objects.get(id=donor.user_id)
    user.delete()
    donor.delete()
    return HttpResponseRedirect('/admin-donor')

@login_required(login_url='adminlogin')
def admin_hospital_view(request):
    hospitals=pmodels.Hospital.objects.all()
    return render(request,'blood/admin_hospital.html',{'hospitals':hospitals})


@login_required(login_url='adminlogin')
def update_hospital_view(request,pk):
    hospital=pmodels.Hospital.objects.get(id=pk)
    user=pmodels.User.objects.get(id=hospital.user_id)
    userForm=pforms.HospitalForm(instance=user)
    hospitalForm=pforms.HospitalForm(request.FILES,instance=hospital)
    mydict={'userForm':userForm,'hospitalForm':hospitalForm}
    if request.method=='POST':
        userForm=pforms.HospitalUserForm(request.POST,instance=user)
        hospitalForm=pforms.HospitalForm(request.POST,request.FILES,instance=hospital)
        if userForm.is_valid() and hospitalForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            hospital=hospitalForm.save(commit=False)
            hospital.user=user
            hospital.blood_group=hospitalForm.cleaned_data['blood_group']
            hospital.save()
            return redirect('admin-hospital')
    return render(request,'blood/update_hospital.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_hospital_view(request,pk):
    hospital=pmodels.Hospital.objects.get(id=pk)
    user=User.objects.get(id=hospital.user_id)
    user.delete()
    hospital.delete()
    return HttpResponseRedirect('/admin-hospital')

@login_required(login_url='adminlogin')
def admin_request_view(request):
    requests = bmodels.BloodRequest.objects.filter(status='Pending')
    return render(request, 'blood/admin_request.html', {'requests': requests})


@login_required(login_url='adminlogin')
def admin_request_history_view(request):
    requests = models.BloodRequest.objects.exclude(status='Pending')
    return render(request, 'blood/admin_request_history.html', {'requests': requests})

@login_required(login_url='adminlogin')
def admin_donation_view(request):
    donations=dmodels.BloodDonate.objects.all()
    return render(request,'blood/admin_donation.html',{'donations':donations})

@login_required(login_url='adminlogin')
def update_approve_status_view(request, pk):
    try:
        req = models.BloodRequest.objects.get(id=pk)
        blood_group = req.blood_group
        unit = req.unit
        message = None

        try:
            stock = models.Stock.objects.get(blood_group=blood_group)
        except models.Stock.DoesNotExist:
            message = f"No stock available for blood group {blood_group}."
            req.status = "Rejected"
            req.save()
        else:
            if stock.unit >= unit:
                req.status = "Approved"  # Just approve, don't reduce stock here
            else:
                message = f"Not enough stock to approve this request. Only {stock.unit} units available."
                req.status = "Rejected"
            req.save()

        requests = models.BloodRequest.objects.filter(status='Pending')
        return render(request, 'blood/admin_request.html', {'requests': requests, 'message': message})

    except models.BloodRequest.DoesNotExist:
        messages.error(request, "Blood request not found.")
        return redirect('admin-request')



@login_required(login_url='adminlogin')
def update_reject_status_view(request,pk):
    req=models.BloodRequest.objects.get(id=pk)
    req.status="Rejected"
    req.save()
    return HttpResponseRedirect('/admin-request')




@login_required(login_url='adminlogin')
def approve_donation_view(request, pk):
    donation = get_object_or_404(BloodDonate, id=pk)

    if request.method == 'POST':
        donation.status = 'Approved'
        donation.appointment_date = request.POST['appointment_date']
        donation.appointment_time = request.POST['appointment_time']
        donation.location = request.POST['location']
        donation.save()
        return redirect('admin-donation')

    return render(request, 'blood/admin_approve_donation.html', {'donation': donation})


@login_required(login_url='adminlogin')
def complete_donation_view(request, pk):
    donation = dmodels.BloodDonate.objects.get(id=pk)
    donation_blood_group = donation.blood_group
    donation_blood_unit = donation.unit

    stock = models.Stock.objects.get(blood_group=donation_blood_group)
    stock.unit = stock.unit + donation_blood_unit
    stock.save()

    donation.status = 'Donated'
    donation.save()

    return HttpResponseRedirect('/admin-donation')



@login_required(login_url='adminlogin')
def reject_donation_view(request,pk):
    donation=dmodels.BloodDonate.objects.get(id=pk)
    donation.status='Rejected'
    donation.save()
    return HttpResponseRedirect('/admin-donation')


@login_required(login_url='adminlogin')
def dispatch_blood(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)

    if blood_request.status == 'Approved' and not blood_request.dispatched:
        try:
            stock = Stock.objects.get(blood_group=blood_request.blood_group)
        except Stock.DoesNotExist:
            messages.error(request, 'Stock not found for the requested blood group.')
            return redirect('admin-request-history')

        if stock.unit >= blood_request.unit:
            stock.unit -= blood_request.unit
            stock.save()

            blood_request.dispatched = True
            blood_request.dispatch_date = timezone.now()
            blood_request.save()

            messages.success(request, 'Blood dispatched successfully.')
        else:
            messages.error(request, f'Insufficient stock to dispatch. Only {stock.unit} units available.')
    else:
        messages.warning(request, 'Invalid dispatch attempt.')

    return redirect('admin-request-history')


@login_required(login_url='adminlogin')
def donation_camps_list_view(request):
    camps = DonationCamp.objects.all().order_by('date')
    return render(request, 'blood/donation_camps_list.html', {'camps': camps})

from django.contrib import messages


def add_donation_camp(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        location = request.POST.get('location')
        description = request.POST.get('description')

        if name and date and location:
            DonationCamp.objects.create(
                name=name,
                date=date,
                location=location,
                description=description
            )
            messages.success(request, 'Donation Camp added successfully!')
            return redirect('admin-donation-camps')
        else:
            messages.error(request, 'Please fill all the required fields.')
    return render(request, 'blood/add_donation_camp.html')
 

def edit_donation_camp(request, camp_id):
    camp = DonationCamp.objects.get(id=camp_id)

    if request.method == 'POST':
        camp.name = request.POST.get('name')
        camp.date = request.POST.get('date')
        camp.location = request.POST.get('location')
        camp.description = request.POST.get('description')
        camp.save()
        messages.success(request, 'Donation Camp updated successfully!')
        return redirect('admin-donation-camps')

    return render(request, 'blood/edit_donation_camp.html', {'camp': camp})


def delete_donation_camp(request, camp_id):
    camp = DonationCamp.objects.get(id=camp_id)
    camp.delete()
    messages.success(request, 'Donation Camp deleted successfully!')
    return redirect('admin-donation-camps')