from django.test import TestCase, Client
from .forms import SignUpForm
import string
from django.contrib.auth.models import User


class IndexPageTests(TestCase):
    def setUp(self):
        self.c = Client()

    def test_index_page_template_render(self):
        """Tests that the correct template would be rendered."""
        response = self.c.get("")
        self.assertTemplateUsed(response, 'accounts/index.html')


class SignUpFormTests(TestCase):
    # -------------------- The tests of the 'username' field --------------------

    def test_username_requirement(self):
        """Tests the 'requirement' of the username field."""
        self.assertFormError(
            SignUpForm({}),
            "username",
            errors="نام کاربری الزامی می‌باشد."
        )

    def test_username_minimum_length(self):
        """Ensures the 'minimum length' of the username field."""
        self.assertFormError(
            SignUpForm({
                "username": "abc"
                }),
            "username",
            errors="نام کاربری باید حداقل 4 و حداکثر 150 کاراکتر باشد."
        )

    def test_username_allowed_characters(self):
        """Ensures that only the allowed characters can be used in a username."""
        prohibited_chars = [punc for punc in string.punctuation if punc not in "@+-_."]
        prohibited_chars.append(" ")
        persian_alpha = [
            "ا", "ب", "پ", "ت", "ث", "ج", "چ", "ح", "خ",
            "د","ذ", "ر", "ز", "ژ", "س", "ش", "ص", "ض",
            "ط", "ظ", "ع", "غ", "ف", "ق", "ک", "گ", "ل",
            "م", "ن", "و", "ه", "ی",
        ]
        prohibited_chars.extend(persian_alpha)
        for char in prohibited_chars:
            username = "ab" + f"{char}" + "cd"
            self.assertFormError(
                SignUpForm({
                    "username": username
                }),
                "username",
                errors="فقط از حروف الفبا و اعداد انگلیسی و نمادهای [@.-_+] استفاده شود."
            )

    def test_username_duplication(self):
        """Prevents the 'duplication' of the usernames."""
        self.test_user = User.objects.create_user("Dr.David@")
        self.assertFormError(
            SignUpForm({
                "username": self.test_user.username.lower()
            }),
            "username",
            errors="این نام کاربری قبلا ثبت شده است."
        )


    # -------------------- The tests of the 'email' field --------------------

    def test_email_requirement(self):
        """Tests the 'requirement' of the email field."""
        self.assertFormError(
            SignUpForm({}),
            "email",
            errors="ایمیل الزامی می‌باشد."
        )

    def test_email_structure(self):
        """Tests the 'structure' of the emails."""
        self.assertFormError(
            SignUpForm({
                "email": "aaa"
            }),
            "email",
            errors="آدرس ایمیل نامعتبر می‌باشد."
        )

    def test_email_duplication(self):
        """Prevents the 'duplication' of the emails."""
        self.test_user2 = User.objects.create_user("garza", "garza@mail.com")
        self.assertFormError(
            SignUpForm({
                "email": self.test_user2.email
            }),
            "email",
            errors="این آدرس ایمیل قبلا ثبت شده است."
        )


    # -------------------- The tests of the 'password' field --------------------

    def test_password_requirement(self):
        """Tests the 'requirement' of the password field."""
        self.assertFormError(
            SignUpForm({}),
            "password",
            errors="رمز عبور الزامی می‌باشد."
        )

    def test_password_minimum_length(self):
        """Ensures the 'minimum length' of the password field."""
        self.assertFormError(
            SignUpForm({
                "password": "pF8@AtN"
            }),
            "password",
            errors="رمز عبور باید حداقل 8 کاراکتر باشد."
        )

    def test_password_personal_info_similarity(self):
        """Makes sure that the password is not too similar to the username or the email."""
        self.assertFormError(
            SignUpForm({
                "username": "david",
                "password": "daviddavi"
            }),
            "password",
            errors="رمز عبور وارد شده مشابهت بالایی با شناسه کاربری یا ایمیل دارد."
        )
        self.assertFormError(
            SignUpForm({
                "email": "garza@gmail.com",
                "password": "garzagarz"
            }),
            "password",
            errors="رمز عبور وارد شده مشابهت بالایی با شناسه کاربری یا ایمیل دارد."
        )

    def test_password_not_common(self):
        """Tests that the password is not a common password."""
        self.assertFormError(
            SignUpForm({
                "password": "abcdefgh"
            }),
            "password",
            errors="رمز عبور وارد شده جزو رمزعبورهای رایج است."
        )

    def test_password_not_entirely_numeric(self):
        """Ensures that the password is not entirely numeric."""
        self.assertFormError(
            SignUpForm({
                "password": "254126968730387489752035724511456245262359895868204"
            }),
            "password",
            errors="رمز عبور وارد شده تماماً عددی است."
        )


    # -------------------- The tests of the 'password_confirmation' field --------------------

    def test_password_confirmation_requirement(self):
        """Tests the 'requirement' of the password_confirmation field."""
        self.assertFormError(
            SignUpForm({}),
            "password_confirmation",
            errors="تکرار رمز عبور الزامی می‌باشد."
        )

    def test_password_confirmation_confirmation(self):
        """Tests the confirmation of the password_confirmation"""
        self.assertFormError(
            SignUpForm({
                "password": "K=Hn)-[q2E",
                "password_confirmation": "K=Hn)@[q2E",
            }),
            "password_confirmation",
            errors="رمزعبور صحیح نمی‌باشد."
        )
