from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
import uuid 
import core.models


# Create your models here.
class User(AbstractBaseUser, core.models.Log):
    username = models.CharField(max_length=200, unique=True)
    USERNAME_FIELD = 'username'
    hash = models.UUIDField(null=True, default=uuid.uuid4)
    email = models.EmailField(null=True, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    birth_date = models.DateField(null=True)
    objects = BaseUserManager()
    is_first_access = models.BooleanField(default=True, null=True)
    user_type = models.CharField(max_length=50, null=True)
    team = models.ForeignKey('team.Team', on_delete=models.DO_NOTHING, null=True)
    height = models.IntegerField(null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    gender = models.CharField(max_length=50, null=True)
    age = models.IntegerField(null=True)


    class Meta:
        db_table = u'user'