from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import TeacherProfile, DirectorProfile

@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:
            DirectorProfile.objects.create(user=instance)  # директор
        else:
            TeacherProfile.objects.create(user=instance)  # учитель
