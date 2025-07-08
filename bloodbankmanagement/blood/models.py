from django.db import models
from hospital import models as pmodels
from donor import models as dmodels
from django.db import models
from datetime import date


class Stock(models.Model):
    blood_group=models.CharField(max_length=10)
    unit=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.blood_group

class BloodRequest(models.Model):
    request_by_hospital=models.ForeignKey(pmodels.Hospital,null=True,on_delete=models.CASCADE)
    request_by_donor=models.ForeignKey(dmodels.Donor,null=True,on_delete=models.CASCADE)
    
    reason=models.CharField(max_length=500)
    blood_group=models.CharField(max_length=10)
    unit=models.PositiveIntegerField(default=0)
    status=models.CharField(max_length=20,default="Pending")
    dispatched = models.BooleanField(default=False)  
    dispatch_date = models.DateTimeField(null=True, blank=True)  

    date=models.DateField(auto_now=True)
    
    def __str__(self):
        return self.blood_group

 

from django.db import models
from datetime import date

class DonationCamp(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()

    def _str_(self):
        return self.name
    
    def is_upcoming(self):
        return self.date>=date.today()
