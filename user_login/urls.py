from django.urls import path
from . import views
from .views import (
    registration_view
)

urlpatterns = [
    path('register/', registration_view , name='register')
]
