from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_user),
    path('signup', views.signup),
    path('verifytoken', views.verify_token),
    path('users', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),
    path('admin/users', views.AdminUserList.as_view())
]