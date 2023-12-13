from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AdvUser, Application, Category
from django.contrib.auth.models import User
from .forms import UserRegistrationForm

admin.site.register(Application)
admin.site.register(Category)


class AdvUserAdmin(UserAdmin):
    add_form = UserRegistrationForm

    list_display = ('username', 'email', 'fullname')
    list_filter = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'fullname', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',)})
    )


admin.site.register(AdvUser, AdvUserAdmin)
