from django.urls import path
from . import views

urlpatterns = [
    path('verify_user', views.UserVerification.as_view())
]