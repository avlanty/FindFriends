from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Member, Profile

@receiver(post_save, sender=Member)
def create_or_save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(member=instance)
    else:
        instance.profile.save()
