from django.contrib import admin

from .models import Beer


@admin.register(Beer)
class BeerAdmin(admin.ModelAdmin):
    fields = (
        "id",
        "name",
        "country",
        "description",
        "points",
        "price",
        "style",
        "brewery",
    )
    list_display = (
        "id",
        "name",
        "country",
        "points",
        "price",
        "style",
        "brewery",
    )
    list_filter = (
        "name",
        "country",
        "style",
        "brewery",
    )
    ordering = ("style",)
    readonly_fields = ("id",)
