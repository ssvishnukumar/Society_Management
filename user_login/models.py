from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractUser
from django.urls import reverse
from more_itertools import first
from pyparsing import Char


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
            username =  username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email), # normalize makes the capital letters small
            # normalize_email is available in BaseUserManager class .
            username=username,
            password=password,
        )
        
        user.is_admin =True
        user.is_staff =True
        user.is_superuser =True
        user.save(using=self._db)
        return user


class Account(AbstractUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=50, unique=True)
    username = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField( max_length=100)
    # middle_name = models.CharField(max_length=100, null=False, default='Kumar')
    mobile_no = models.CharField( max_length=15)
    tower_no=models.CharField( max_length=10)
    flat_no = models.CharField( max_length=10)
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

    # def has_perm(self, perm, obj=None):
    #     return self.is_admin

    def has_module_perm(self, app_label):
        return True
    
    # if user.is_active


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class News(models.Model):
    title = models.CharField(max_length=200, unique=True)
    # slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(Account, on_delete= models.CASCADE)
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=1)    
    
    class Meta:
        ordering = ['-created_on']
        
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('user_login:user_dashboard')
    
    
    
BHK = (
    (1,'1BHK'),
    (2,'2BHK'),
    (3,'3BHK'),
) 

FURNISHED = (
    (0, 'Not Furnished'),
    (1, 'FURNISHED'),
)

class BuyRent(models.Model):    
    email = models.EmailField(verbose_name='email', max_length=50, unique=False)
    username = models.CharField(max_length=200, unique=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField( max_length=100)
    
    mobile_no = models.CharField(max_length=11)
    buy_flat = models.BooleanField(default=False)
    rent_flat = models.BooleanField(default=False)
    
    flat_type = models.IntegerField(choices=BHK, default=1)
    # flat_type = models.CharField(max_length=10)
    pool = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    creche = models.BooleanField(default=False)
    
    cleaning_house = models.BooleanField(default=False)
    furnished = models.IntegerField(choices=FURNISHED, default=0)
    
    no_of_members = models.IntegerField(default=1)

    # emi = models.BooleanField(default=False)
    
class Visitors(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    mobile_no = models.CharField(max_length=15)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)


choose = (
    (0, 'Complaint'),
    (1, 'Suggestion'),
)
class ComplaintSuggestion(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    choose = models.IntegerField(choices=choose ,default=0)
    
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)


    