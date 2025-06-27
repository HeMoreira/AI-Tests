from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ('N', 'Prefer not to say'),
]

class Customer(AbstractUser):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    registration_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.username