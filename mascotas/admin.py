from django.contrib import admin
from .models import *
# Register your models here.

from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ("dni","email", "first_name", "last_name", "is_staff")
    search_fields = ("dni","email", "first_name", "last_name")
    ordering = ("dni",)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "dni",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    
                    "is_veterinario",
                    "is_provedor"
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("dni","first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "is_veterinario",
                    "is_provedor",
                    
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
admin.site.register(CustomUser,CustomUserAdmin)

admin.site.register(Mascota)
admin.site.register(HistoriaMedica)
admin.site.register(Provedor)
admin.site.register(Producto)
admin.site.register(Category)
admin.site.register(Appointment)