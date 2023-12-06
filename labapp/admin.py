from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


class MyUserInline(admin.StackedInline):
    model = UserBasic
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (MyUserInline,)


admin.site.site_header = '实验室后台管理'

# User
admin.site.register(UserBasic)
admin.site.register(UserDetails)

# lab
admin.site.register(Laboratory)

# actions
admin.site.register(Application)
admin.site.register(Recruitment)
