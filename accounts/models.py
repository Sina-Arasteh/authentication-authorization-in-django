from django.db import models
from django.contrib.auth.models import User


class PremiumUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    is_premium = models.BooleanField('کاربر ویژه', default=False)

    def __str__(self):
        return self.user.username
