import os
from django.db import models
from django.conf import settings

# os.path('.')

from users.models import Student,Club

class Event(models.Model):

    
    name = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='images/')
    Description = models.TextField(max_length=1000,null=True)
    SpokePerson = models.CharField(max_length = 20,null=True)
    venue = models.CharField(max_length=50)
    timeDate = models.DateTimeField(auto_now=False, auto_now_add=False)
    formLink = models.URLField(null=True)
    club = models.ForeignKey(Club,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name + " "+str(self.timeDate)


class EventRegistraion(models.Model):

    evnetName = models.ForeignKey(Event, on_delete=models.CASCADE,related_name='event')
    name = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='users')
    attend = models.BooleanField(default=False)
    conform = models.BooleanField(default=True)