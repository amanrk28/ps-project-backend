from django.urls import path
from . import views

urlpatterns = [
    path('verify_user', views.verify_user_and_return_token),
    path('signup', views.signup),
    path('users', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),
    path('admin/users', views.AdminUserList.as_view())
]