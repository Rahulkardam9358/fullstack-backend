from django.contrib import admin
from authentication.models import User, Address
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseAdmin):
    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", )}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff",)
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)


admin.site.register(User, UserAdmin)
admin.site.register(Address)
