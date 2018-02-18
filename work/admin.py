from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline, ]
    def sex(obj):
        return obj.profile.sex
    def year(obj):
        return obj.profile.year
    sex.short_description = 'sex'
    year.short_description = 'year'
    list_display = ['username','email',sex,year]

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','email','number']
    list_editable = ['number']
    class Meta:
        model = contact

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
# Register your models here.
admin.site.register(contact,ContactAdmin)
admin.site.unregister(Group)

