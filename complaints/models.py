from django.db import models
# Create your models here.

class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('water', 'Water Wastage'),
        ('e_waste', 'E-Waste'),
        ('solid_waste', 'Solid/Garbage Waste'),
        ('animal_injury', 'Injured/Sick Animal'),
        ('others','Others'),
        
    ]

    name = models.CharField(max_length=15)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=255, help_text="Area in Ahmedabad")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='complaint_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.get_category_display()} - {self.location}"

from django.db import models
from django.utils import timezone

class WasteLog(models.Model):
    HAZARD_TYPES = [
        ('plastic', 'Accumulated Plastic / Garbage Dump'),
        ('ewaste', 'Electronic / Chemical Waste'),
        ('water', 'Stagnant Water / Drainage Leak'),
        ('animal_risk', 'High Wildlife/Stray Injury Risk Zone'),
    ]
    
    title = models.CharField(max_length=200)
    hazard_type = models.CharField(max_length=20, choices=HAZARD_TYPES)
    description = models.TextField()
    # Coordinates for mapping
    latitude = models.FloatField()
    longitude = models.FloatField()
    reported_at = models.DateTimeField(default=timezone.now)
    is_cleared = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_hazard_type_display()} at ({self.latitude}, {self.longitude})"
    

from django.db import models

class AnimalHospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_24_7 = models.BooleanField(default=False)
    open_time = models.CharField(max_length=50, default="09:00 AM")
    close_time = models.CharField(max_length=50, default="08:00 PM")

    def __str__(self):
        return self.name