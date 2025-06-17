from django.contrib import admin

from . import models

@admin.register(models.Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'is_active', 'valid_from', 'valid_to']
    list_filter = ['is_active', 'valid_from', 'valid_to']
    search_fields = ['code']