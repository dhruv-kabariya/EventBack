from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser
from django.conf import settings

# Create your models here.


class Student(AbstractUser):
    # class Meta:
    #     db_table = 'auth_user'

    club = models.BooleanField(default=False)
    avtar = models.ImageField(
        upload_to='avtars/',null=True)

    def __str__(self):
        return self.username


class Club(models.Model):

    name = models.CharField(max_length=50)
    logo = models.ImageField(
        upload_to='clubLogo/', default="/avtars/profile.jpg")
    description = models.TextField(max_length=1000, default='')

    def __str__(self):
        return self.name


class Membership(models.Model):

    name = models.ForeignKey(Student , on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    position = models.CharField(max_length=20)

    def __str__(self):
        return self.name.username + "  " + self.club.name
