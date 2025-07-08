from django.db import models
from django.contrib.auth.models import User

class Donor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Donor/',null=True,blank=True)

    
    blood_group=models.CharField(max_length=10)
    

    address = models.CharField(max_length=41)
    mobile = models.CharField(max_length=20,null=False)
   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.get_name 

class BloodDonate(models.Model): 
    donor=models.ForeignKey(Donor,on_delete=models.CASCADE)   
    disease=models.CharField(max_length=100,default="Nothing")
    age=models.PositiveIntegerField()
    blood_group=models.CharField(max_length=10)
    unit=models.PositiveIntegerField(default=0)
    status=models.CharField(max_length=20,default="Pending")
    date=models.DateField(auto_now=True)
    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    
    def __str__(self):
        return self.donor