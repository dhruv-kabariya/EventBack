from django import forms
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from .models import Student

class StudnetCreationForm(UserCreationForm):

    class Meta:
        model = Student
        fields = ("username","email")

class StudnetChangeForm(UserChangeForm):

    class Meta:
        model = Student
        fields = ("username","email")
        