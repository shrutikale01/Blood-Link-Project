from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import DonationCamp

class DonationCampAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'description')  # Use 'name' instead of 'title'
    search_fields = ('name', 'location')
    list_filter = ('date', 'location')

admin.site.register(DonationCamp, DonationCampAdmin)
