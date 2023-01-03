from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from django.http import request
import datetime
from dateutil.relativedelta import *


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email,user_type=None, password=None,  is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users must have a valid email')
        if not password:
            raise ValueError("You must enter a password")

        email = self.normalize_email(email)
        user_obj = self.model(email=email)
        user_obj.set_password(password)
        user_obj.user_type = user_type
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, user_type=None, password=None):
        user = self.create_user(
            email, user_type=user_type, password=password, is_staff=True)
        return user

    def create_superuser(self, email, user_type='admin', password=None):
        user = self.create_user(email, user_type=user_type,password=password, is_staff=True, is_admin=True)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    user_type = models.CharField(max_length=255,null=True, blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # def __str__(self):
    #     return self.email+' ' + str(self.id)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

class Client(models.Model):
    user = models.ForeignKey('User',on_delete=models.SET_NULL, null=True,blank=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
         return self.name

class Firm(models.Model):
    user = models.ForeignKey('User',on_delete=models.SET_NULL, null=True,blank=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
         return self.name

class Lawyer(models.Model):
    user = models.ForeignKey('User',on_delete=models.SET_NULL, null=True,blank=True)
    firm = models.ForeignKey('Firm',on_delete=models.SET_NULL, null=True,blank=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
         return self.name

class Case(models.Model):
    client = models.ForeignKey('Client',on_delete=models.SET_NULL, null=True, blank=True)
    firm = models.ForeignKey('Firm',on_delete=models.SET_NULL, null=True,blank=True)
    subject = models.CharField(max_length=255,null=True,blank=True)
    area = models.CharField(max_length=255,null=True,blank=True)
    proof = models.ImageField(null=True,blank=True,upload_to='media/')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True,blank=True,null=True)


    def __str__(self):
         return self.subject