from django.contrib import admin
from django.contrib.auth import  get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import StudnetChangeForm,StudnetCreationForm
from .models import Student,Club,Membership
# Register your models here.

class StudentAdmin(UserAdmin):

    add_form = StudnetCreationForm
    form = StudnetChangeForm
    model = Student
    list_display = ['email','username']

# admin.site.register(Student,UserAdmin)
admin.site.register(Student)
admin.site.register(Club)
admin.site.register(Membership)