from django.db import models
from django.contrib.auth.models import User

class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/Hospital/', null=True, blank=True)

    hospital_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100, unique=True)
    contact_person = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20, null=False)

    @property
    def get_name(self):
        return self.hospital_name  # Since hospitals don't have first/last names

    def __str__(self):
        return self.hospital_name
