from django.contrib import admin

from .models import Beer


@admin.register(Beer)
class BeerAdmin(admin.ModelAdmin):
    fields = (
        "id",
        "country",
        "description",
        "points",
        "price",
        "style",
        "brewery",
    )
    list_display = (
        "id",
        "country",
        "points",
        "price",
        "style",
        "brewery",
    )
    list_filter = (
        "country",
        "style",
        "brewery",
    )
    ordering = ("style",)
    readonly_fields = ("id",)
