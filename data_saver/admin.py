from django.contrib import admin

from .models import Brand, BrandDetails


# @admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'price']

    admin.site.register(Brand)
    admin.site.register(BrandDetails)
