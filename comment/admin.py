from django.contrib import admin

# Register your models here.
from django.contrib import admin

from . import models

# Register your models here.
class Comment(admin.ModelAdmin):
    list_display = ("id", "body", "created_at")


admin.site.register(models.Comment, Comment)
