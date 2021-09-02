import os
import binascii
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from project_backend.settings import AUTH_USER_MODEL

class UserManager(BaseUserManager):
    # custom user model
    def __init__(self, *args, **kwargs):
        self.with_inactive = kwargs.pop('inactive', False)
        super(BaseUserManager, self).__init__(*args, **kwargs)

    def create_user(self, email, password, phone_number='', is_active=False, is_admin=False, is_staff=False):
        # Create user
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), phone_number=phone_number)
        user.is_active = is_active
        user.is_admin = is_admin
        user.is_staff = is_staff
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, phone_number):
        # Create a superuser
        user = self.create_user(email, password, phone_number=phone_number, is_active=True, is_admin=True, is_staff=True)
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        qs = super(UserManager, self).get_queryset(*args, **kwargs)
        if self.with_inactive:
            return qs
        else:
            return qs.filter(is_active=True)


def get_address():
    return {'house_no': '', 'street': '', 'city': '', 'pincode': ''}

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=21, null=True, blank=True)
    username = models.CharField(max_length=128, null=True, unique=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_store_owner = models.BooleanField(default=False)
    address = models.JSONField(default=get_address)
    objects = UserManager()
    all_objects = UserManager(inactive=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return '%s, %s' % (self.id, self.username)

    @property
    def fullname(self):
        return (getattr(self, 'first_name') or '') + ' ' + (getattr(self, 'last_name') or '')

class AuthToken(models.Model):
    key = models.CharField(_("Key"), max_length=40, db_index=True, unique=True)
    user = models.ForeignKey(AUTH_USER_MODEL, related_name="auth_tokens", on_delete=models.CASCADE, verbose_name=_("User") )

    class Meta:
        verbose_name = "token"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()