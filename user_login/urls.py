from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views

from .views import (
    logout_view, login_view, registration_view, otp_view, dashboard_view
)


app_name = 'user_login'
urlpatterns = [
    path('register/', registration_view, name='register' ),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('otp/', otp_view, name='otp'),
    path("dashboard/", dashboard_view, name="dashboard"),


    # path('reset_password/', auth_views.PasswordResetView().as_view(), name='reset')
    ]

