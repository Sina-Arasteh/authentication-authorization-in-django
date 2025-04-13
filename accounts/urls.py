from django.urls import path
from . import views, forms
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('', views.index_page, name="index"),
    path('signup/', views.signup, name="signup"),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=forms.CustomAuthenticationForm
        ),
        name="login"
    ),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signup-successful/', views.signup_successful, name="successfulsignup"),
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            form_class=forms.CustomPasswordChangeForm,
            template_name="accounts/password_change_form.html",
            success_url="password-change-done"
        ),
        name="password_change"
    ),
    path(
        'password-change-done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ),
        name="password_change_done"
    ),
]
