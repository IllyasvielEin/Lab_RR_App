from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
from .models.user import UserBasic


admin.site.site_header = '实验室后台管理'

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserInline(admin.StackedInline):
    model = UserBasic
    can_delete = False
    verbose_name_plural = 'user'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserInline, )


admin.site.unregister(User)
# User
admin.site.register(User, UserAdmin)
admin.site.register(UserDetails)

# lab
admin.site.register(Laboratory)

# actions
admin.site.register(Application)
admin.site.register(Recruitment)
