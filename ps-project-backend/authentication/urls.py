from django.urls import path
from . import views

urlpatterns = [
    path('verify_user', views.verify_user_and_return_token),
    path('signup', views.signup),
]