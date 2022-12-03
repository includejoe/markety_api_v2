from django.contrib import admin

from . import models

# Register your models here.
class Post(admin.ModelAdmin):
    list_display = (
        "id",
        "category",
        "name",
        "description",
        "price",
        "condition",
        "image1",
        "image2",
        "image3",
        "is_sold",
        "created_at",
        "updated_at",
    )


admin.site.register(models.Post, Post)
