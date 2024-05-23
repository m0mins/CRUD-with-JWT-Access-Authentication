from django.db import models

# To Create a Custom User Model and Admin Panel

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy

# To automatically create one to one objects

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class UserRole(models.Model):
    ROLE_CHOICES = [
        ('is_admin', 'Admin'),
        ('is_staff', 'Staff'),
        ('is_user', 'User')
    ]
    role = models.CharField(max_length=50,unique=True, choices=ROLE_CHOICES, default='user')
    def __str__(self):
        return self.role


class MyUserManager(BaseUserManager):
    """ A custom Manager to deal with emails as unique identifer """
    def _create_user(self, email, password,**extra_fields):
    #def _create_user(self, email, password,role=None,**extra_fields):

        """ Creates and saves a user with a given email and password"""

        if not email:
            raise ValueError("The Email must be set!")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

        #if role:
        #    user.role = role
        #user.save(using=self._db)
        #return user


    #def create_user(self, email, password=None, **extra_fields):
    #    return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username= models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(unique=True, null=False)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_role')
    auth_token=models.CharField(max_length=100, blank=False)
    is_varified = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        gettext_lazy('staff status'),
        default=False,
        help_text = gettext_lazy('Designates whether the user can log in this site')
    )

    is_active = models.BooleanField(
        gettext_lazy('active'),
        default=True,
        help_text=gettext_lazy('Designates whether this user should be treated as active. Unselect this instead of deleting accounts')
    )

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
    
    # if you want to set role as unique
    #class Meta:
    #    unique_together = ('role',)


class Document(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    uploaded_file=models.FileField(upload_to='files')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class TodoItem(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    uploaded_file=models.FileField(upload_to='filess', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='userR')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.title