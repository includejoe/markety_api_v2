from django.contrib import admin

from . import models

# Register your models here.
class User(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "username",
        "phone",
        "dob",
    )


admin.site.register(models.User, User)
