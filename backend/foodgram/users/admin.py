from django.contrib import admin
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'role',
    )
    search_fields = (
        'email',
        'username',
    )
    list_filter = (
        'email',
        'username',
    )
    list_editable = (
        'username',
        'email',
    )

