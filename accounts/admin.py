from django.contrib import admin
from django.apps import apps
from .models import PremiumUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


models = apps.get_models()
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

admin.site.unregister(PremiumUser)

class PremiumUserInline(admin.StackedInline):
    model = PremiumUser
    can_delete = False

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [PremiumUserInline]
