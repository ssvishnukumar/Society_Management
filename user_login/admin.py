from django.contrib import admin
from user_login.models import Account, UserOTP
from django.contrib.auth.admin import UserAdmin

# admin.site.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username','date_joined', 'last_login','is_admin','is_staff')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = () # I think we will get error without this fieldsets

admin.site.register(Account, AccountAdmin)
