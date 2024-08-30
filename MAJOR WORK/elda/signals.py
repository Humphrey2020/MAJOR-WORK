from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, StaffProfile, CandidateProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'staff':
            StaffProfile.objects.create(user=instance, full_name=instance.first_name, email=instance.email)
        elif instance.user_type == 'candidate':
            CandidateProfile.objects.create(user=instance, full_name=instance.first_name, email=instance.email)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 'staff':
        instance.staffprofile.save()
    elif instance.user_type == 'candidate':
        instance.candidateprofile.save()
