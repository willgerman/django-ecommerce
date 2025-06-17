from django.contrib import admin

# Register your models here.
from organization import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", 'date_created', 'date_updated']
    list_display_links = ["name",]
    prepopulated_fields = {
        "slug": ("name",),
    }
    search_fields = ("name",)
    list_per_age = 25
    ordering = ["date_created"]