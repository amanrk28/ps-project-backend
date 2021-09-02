# User manager model module
from django.contrib.auth.models import BaseUserManager

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
