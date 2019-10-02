from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='images/', default='images/boy.png')
    dob = models.DateField(max_length=8, null=True, blank=True)
    aMyself = models.TextField(null=True, blank=True)
