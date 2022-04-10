from enum import unique

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class MyAccountManager(BaseUserManager): # This function is created after the Account class is created.
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Every User should have email address ")
        if not username:
            raise ValueError("Every User should have username")
        # if all of the above fields are given, then

        user = self.model(
            email=self.normalize_email(email), # normalize makes the capital letters small
            # normalize_email is available in BaseUserManager class .
            username=  username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email), # normalize makes the capital letters small
            # normalize_email is available in BaseUserManager class .
            username=  username,
            password=password,
        )
        user.is_admin =True
        user.is_staff =True
        user.is_superuser =True
        user.save(using=self._db)
        return user





class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=50, unique=True)
    username = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField( max_length=100)
    # middle_name = models.CharField(max_length=100, null=False, default='Kumar')
    # mobile_no = models.IntegerField(default=0)
    # tower_no=models.IntegerField(default=0)
    # flat_no = models.IntegerField(default=0)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login',auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default= False)
    # otp = models.CharField(max_length=6, null=True, blank=True)




    USERNAME_FIELD = 'email' # here username field is a keyword. So don't get confused.
    # basically this is a login field.

    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager() # here we are telling that where the manager is (i.e) AccountManager.

    def __str__(self):
        return self.username + ' | ' + self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perm(self, app_label):
        return True


class UserOTP(models.Model):
    user=models.ForeignKey(Account, on_delete=models.CASCADE)
    time_st=models.DateTimeField(auto_now=True)
    otp=models.SmallIntegerField()


