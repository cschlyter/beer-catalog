from django.urls import path

from .views import BeersView

urlpatterns = [
    path("beers/", BeersView.as_view()),
]
