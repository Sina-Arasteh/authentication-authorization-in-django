from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
import re


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        min_length=4,
        error_messages={
            "required": "نام کاربری الزامی می‌باشد.",
            "max_length": "نام کاربری باید حداقل 4 و حداکثر 150 کاراکتر باشد.",
            "min_length": "نام کاربری باید حداقل 4 و حداکثر 150 کاراکتر باشد.",
        },
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+\Z",
                message="فقط از حروف الفبا و اعداد انگلیسی و نمادهای [@.-_+] استفاده شود.",
                flags=re.A
            )
        ]
    )
    email = forms.EmailField(
        error_messages={
            "required": "ایمیل الزامی می‌باشد.",
            "invalid": "آدرس ایمیل نامعتبر می‌باشد.",
        }
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput,
        error_messages={
            "required": "رمز عبور الزامی می‌باشد.",
            "min_length": "رمز عبور باید حداقل 8 کاراکتر باشد.",
        }
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            "required": "تکرار رمز عبور الزامی می‌باشد.",
        }
    )

    def clean_username(self):
        """Prevents the duplication of username."""
        username = self.cleaned_data['username']
        try:
            User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return username
        raise ValidationError("این نام کاربری قبلا ثبت شده است.")
        
    def clean_email(self):
        """Prevents the duplication of email."""
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise ValidationError("این آدرس ایمیل قبلا ثبت شده است.")
    
    def clean_password(self):
        """Validates the password through the password validators"""
        password = self.cleaned_data['password']
        try:
            username = self.cleaned_data['username']
        except:
            username = None
        try:
            email = self.cleaned_data['email']
        except:
            email = None
        user = User(
            username=username,
            email=email,
        )
        validate_password(password, user=user)
        return password

    def clean_password_confirmation(self):
        """Checks the similarity of the password_confirmation field to the password field"""
        password = self.cleaned_data['password']
        password_confirmation = self.cleaned_data['password_confirmation']
        if password_confirmation != password:
            raise ValidationError("رمزعبور صحیح نمی‌باشد.")
        return password_confirmation
