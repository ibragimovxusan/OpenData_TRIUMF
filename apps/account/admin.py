from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.account.models import User, Admin, Contact

admin.site.register(User, UserAdmin)
admin.site.register(Admin)
admin.site.register(Contact)
