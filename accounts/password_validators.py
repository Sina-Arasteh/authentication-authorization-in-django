from django.contrib.auth.password_validation import (
    NumericPasswordValidator,
    CommonPasswordValidator,
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
)
from django.core.exceptions import ValidationError


class CustomNumericPasswordValidator(NumericPasswordValidator):
    def get_error_message(self):
        return "رمز عبور وارد شده تماماً عددی است."

class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def get_error_message(self):
        return "رمز عبور وارد شده مشابهت بالایی با شناسه کاربری یا ایمیل دارد."

class CustomCommonPasswordValidator(CommonPasswordValidator):
    def get_error_message(self):
        return "رمز عبور وارد شده جزو رمزعبورهای رایج است."

class CustomMinimumLengthValidator(MinimumLengthValidator):
    def get_error_message(self):
        return "رمز عبور باید حداقل 8 کاراکتر باشد."
