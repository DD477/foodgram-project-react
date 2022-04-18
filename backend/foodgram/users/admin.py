from django.contrib import admin

from recipes.admin import EMPTY_VALUE_DISPLAY

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name',
                    'last_name', 'email', 'is_staff')
    fields = (
        ('username',),
        ('password',),
        ('email',),
        ('first_name',),
        ('last_name',),
        ('last_login',),
        ('date_joined',),
        ('is_active',), 
        ('is_superuser',), 
        ('is_staff',),
        ('groups',),
        ('user_permissions',),
    )
    list_editable = ('username', 'first_name',
                     'last_name', 'email', 'is_staff')
    filter_horizontal = ('groups', 'user_permissions',)
    search_fields = ('username', 'email', 'is_staff')
    list_filter = ('email', 'username')

    save_on_top = True

    empty_value_display = EMPTY_VALUE_DISPLAY