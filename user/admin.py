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
        "password",
        "phone",
        "gender",
        "dob",
        "bio",
        "is_vendor",
        "is_active",
        "is_staff",
        "is_verified",
        "created_at",
    )


admin.site.register(models.User, User)
