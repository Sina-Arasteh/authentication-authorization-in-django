from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import PremiumUser


@receiver(
        post_save,
        sender=settings.AUTH_USER_MODEL,
        dispatch_uid="premiumuser_creation_instance"
)
def user_post_save_handler(sender, instance, created, **kwargs):
    if created:
        PremiumUser.objects.create(user=instance)
