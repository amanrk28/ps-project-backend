from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from authentication.user_manager import UserManager

def get_address():
    return {'house_no': '', 'street': '', 'city': '', 'pincode': ''}


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=256, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=21, null=True, blank=True)
    username = models.CharField(max_length=128, null=True, unique=True, blank=True)
    password = models.CharField(max_length=128, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_store_owner = models.BooleanField(default=False)
    address = models.JSONField(default=get_address)
    objects = UserManager()
    all_objects = UserManager(inactive=True)
    USERNAME_FIELD = 'username'

    class Meta:
        unique_together = ('email',)

    def __str__(self):
        return '%s, %s' % (self.id, self.username)

    @property
    def fullname(self):
        return (getattr(self, 'first_name') or '') + ' ' + (getattr(self, 'last_name') or '')