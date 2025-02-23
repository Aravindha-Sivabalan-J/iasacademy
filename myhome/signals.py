from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.apps import apps


@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:
        UserProfile = apps.get_model('myhome', 'UserProfile')  # ✅ FIX: Avoid circular import

        try:
            profile = instance.profile
        except UserProfile.DoesNotExist:
            return  

        if profile.group:
            instance.groups.add(profile.group)  # ✅ Assign group after saving
            instance.save()