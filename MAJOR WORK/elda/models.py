from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('superadmin', 'SuperAdmin'),
        ('staff', 'Staff'),
        ('candidate', 'Candidate'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='candidate')


class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='staff')
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


class Candidate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='candidate')
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    statement_of_purpose = models.TextField()
    selected_university = models.CharField(max_length=255)
    selected_course = models.CharField(max_length=255)



class OTP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)