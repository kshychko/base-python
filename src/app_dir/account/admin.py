from django.contrib import admin

from app_dir.account.models import UserRole, Account

admin.site.register(Account)
admin.site.register(UserRole)
