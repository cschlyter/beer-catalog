from rest_framework.generics import ListAPIView

from .models import Beer
from .serializers import BeerSerializer
from .filters import BeerFilterSet


class BeersView(ListAPIView):
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer
    filterset_class = BeerFilterSet
