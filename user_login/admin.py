from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# admin.site.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username','date_joined', 'last_login','is_admin','is_staff')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = () # I think we will get error without this fieldsets

admin.site.register(Account, AccountAdmin)

# for viewing trhe posts
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    # prepopulated_fields = {'slug': ('title',)}

admin.site.register(News, NewsAdmin)
admin.site.register(BuyRent)