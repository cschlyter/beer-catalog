from django.urls import path

from .views import BeersView, ESBeersView

urlpatterns = [
    path("beers/", BeersView.as_view()),
    path("es-beers/", ESBeersView.as_view()),
]
