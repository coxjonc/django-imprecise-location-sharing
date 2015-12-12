from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import (
AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        user=self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.is_superuser=True
        user.is_admin=True
        user.is_staff=True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=254,
        unique=True,
        null=True
    )
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    newsletter = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def get_full_name(self):
        return self.last_name

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
        return "{}'s account".format(self.email)

class History(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def changed_less_than_one_week_ago(self):
        return self.created_at >= timezone.now() - datetime.timedelta(days=7)