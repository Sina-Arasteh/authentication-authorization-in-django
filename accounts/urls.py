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
]
