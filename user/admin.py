from django.contrib import admin

from . import models

# Register your models here.
class User(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "username",
        "email",
        "phone",
        "gender",
        "dob",
        "bio",
        "country",
        "is_vendor",
        "is_active",
        "is_staff",
        "is_verified",
        "is_blocked",
        "created_at",
    )


admin.site.register(models.User, User)
