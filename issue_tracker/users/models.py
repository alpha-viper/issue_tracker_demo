from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from datetime import date
# Create your models here.


class User(AbstractUser):
    username=None
    password=models.CharField(null=False)
    email=models.EmailField(null=False,unique=True)
    first_name=models.CharField(max_length=50,null=False)
    last_name=models.CharField(max_length=50,null=False)
    dob = models.DateField(default=date.today)
    USERNAME_FIELD='email'
    objects=UserManager()
    REQUIRED_FIELDS=[]
    # projects=models.ManyToManyField(Project)





