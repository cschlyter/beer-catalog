from django.db.models import Q

from django_filters.rest_framework import CharFilter, FilterSet

from .models import Beer


class BeerFilterSet(FilterSet):
    query = CharFilter(method="filter_query")

    def filter_query(self, queryset, name, value):
        search_query = Q(
            Q(style__contains=value)
            | Q(brewery__contains=value)
            | Q(description__contains=value)
            | Q(name__contains=value)
        )
        return queryset.filter(search_query)

    class Meta:
        model = Beer
        fields = (
            "query",
            "country",
            "points",
        )
