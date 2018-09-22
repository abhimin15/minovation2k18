from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','email','number','message']
    list_editable = ['number']
    class Meta:
        model = contact

class CampusAdmin(admin.ModelAdmin):
    list_display = ['name','email','number','wat','college','branch','year']
    #list_editable = ['number','wat']
    class Meta:
        model = CampusAmb

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['name','email','number','wat','college','branch','year','event']
    #list_editable = ['number','wat']
    class Meta:
        model = Registration

# Register your models here.
admin.site.register(contact,ContactAdmin)
admin.site.register(CampusAmb,CampusAdmin)
admin.site.register(Registration,RegistrationAdmin)
admin.site.unregister(Group)

