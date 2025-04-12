from django.shortcuts import render
from . import forms
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse


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
        "signup_form": signup_form
    }
    return render(request, "accounts/signup.html", context)


def login(request):
    return render(request, "accounts/login.html")


def signup_successful(request):
    return render(request, "accounts/successful_signup.html")
