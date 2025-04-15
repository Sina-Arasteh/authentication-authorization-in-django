from django.shortcuts import render
from . import forms
from .models import PremiumUser
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


def index_page(request):
    """Renders the index page."""
    return render(request, 'accounts/index.html')


def signup(request):
    if request.method == "POST":
        signup_form = forms.SignUpForm(request.POST)
        if signup_form.is_valid():
            User.objects.create_user(
                request.POST['username'],
                email = request.POST['email'],
                password = request.POST['password']
            )
            return HttpResponseRedirect(reverse("accounts:successfulsignup"))
    else:
        signup_form = forms.SignUpForm()
    context = {
        "signup_form": signup_form,
    }
    return render(request, "accounts/signup.html", context)


def login(request):
    return render(request, "accounts/login.html")


def signup_successful(request):
    return render(request, "accounts/successful_signup.html")


@login_required
def account_type_change(request):
    user = PremiumUser.objects.get(user=request.user.pk)
    if request.method == "POST":
        if user.is_premium:
            user.is_premium = False
        else:
            user.is_premium = True
        user.save()
    context = {"acctype": user.is_premium,}
    return render(request, "accounts/account_type_change_form.html", context)


def premium_access(user):
    u = PremiumUser.objects.get(user=user.pk)
    return u.is_premium

@login_required
@user_passes_test(premium_access)
def premium_customer_club(request):
    return render(request, "accounts/premium_customer_club.html")

@login_required
def account_delete(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse("accounts:login"))
    return render(request, "accounts/account_delete.html")
