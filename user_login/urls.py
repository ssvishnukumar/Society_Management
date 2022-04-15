from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import (
    logout_view, login_view, registration_view, otp_view, user_dashboard_view, dashboard_view,
newsadd, complaintadd
)


app_name = 'user_login'
urlpatterns = [
    path('register/', registration_view, name='register' ),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    # path('otp/', otp_view, name='otp'),
    path('otpverify/', otp_view, name='otp'),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("user_dashboard/", user_dashboard_view, name="user_dashboard"),


    # path("password_reset/", auth_views.PasswordResetView.as_view(template_name='password_reset1.html'), name="password_reset"),
    # path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done1.html'), name="password_reset_done"),
    # path("password_reset_confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm1.html'), name="password_reset_confirm"),
    # path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete1.html'), name="password_reset_complete"),

    # change password
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name="password_change_done"),
    path("password_change/", auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name="password_change"),

    # reset password
    path("password_change/done/", auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name= 'password_reset'),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name="password_reset_complete"),


    # path('news_list', NewsList.as_view(), name='news_list'),
    path('news/add/', newsadd, name='news_add'),
    # path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    # path('delete/<int:author_id>/<int:id>/', NewsDelete.as_view(), name='news_delete'),
    
    
    path('complaint/add/', complaintadd, name='complaint_add'),
    
    ]

