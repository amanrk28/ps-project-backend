# User manager model module
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    # custom user model
    def __init__(self, *args, **kwargs):
        self.with_inactive = kwargs.pop('inactive', False)
        super(BaseUserManager, self).__init__(*args, **kwargs)

    def create_user(
            self,
            email,
            phone_number,
            password,
            username='',
            is_active=False,
            is_staff=False,
            is_admin=False
    ):
        # Create user
        if not email:
            raise ValueError('Users must have an email address')
        if not phone_number:
            raise ValueError('Users must have an phone number')
        user = self.model(email=self.normalize_email(email))
        user.phone_number = phone_number
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_admin = is_admin
        if username:
            user.username = username
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        # Create a superuser
        if password is None:
            raise TypeError('Superuser must have a password')
        user = self.model(username=username)
        user.set_password(password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        qs = super(UserManager, self).get_queryset(*args, **kwargs)
        if self.with_inactive:
            return qs
        else:
            return qs.filter(is_active=True)
