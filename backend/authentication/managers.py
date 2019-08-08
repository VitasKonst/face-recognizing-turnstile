from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    default_password = 'MethodPro-2019'

    def create_user(self, phone, password=default_password, email='',  **extra_fields):
        if phone is None:
            raise ValueError(_('Users must have a phone.'))

        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, phone, password, **extra_fields):
        if password is None:
            raise ValueError(_('Superusers must have a password.'))

        user = self.create_user(phone, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

