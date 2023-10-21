from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from urllib.parse import SplitResult, urlencode, urlsplit

from . import constants
from .models import Beer
from .serializers import BeerSerializer
from .filters import BeerFilterSet


class BeersView(ListAPIView):
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer
    filterset_class = BeerFilterSet


class ESBeersView(APIView):
    def _build_url(self, params, new_offset):
        url = self.request.build_absolute_uri()
        old_result = urlsplit(url)
        new_result = SplitResult(
            old_result.scheme,
            old_result.netloc,
            old_result.path,
            query=urlencode(
                {
                    **params,
                    "offset": new_offset,
                },
                doseq=True,
            ),
            fragment="",
        )
        return new_result.geturl()

    def _get_previous_page(self, params):
        limit, offset = params.get("limit"), params.get("offset")
        if offset > 0:
            return self._build_url(params, offset - limit)
        else:
            return None

    def _get_next_page(self, params, count):
        limit, offset = params.get("limit"), params.get("offset")
        if (offset + limit) < count:
            return self._build_url(params, offset + limit)
        else:
            return None

    def get(self, request, *args, **kwargs):
        query = self.request.query_params.get("query")
        limit = int(self.request.query_params.get("limit", 10))
        offset = int(self.request.query_params.get("offset", 0))

        # Build Elasticsearch query.
        search = Search(index=constants.ES_INDEX)
        search = search.query(
            "bool",
            should=[
                Match(name=query),
                Match(style=query),
                Match(brewery=query),
                Match(description=query),
            ][offset: offset + limit],
        )

        response = search.execute()

        return Response(
            data={
                "count": response.hits.total.value,
                "next": self._get_next_page(
                    {
                        "limit": limit,
                        "offset": offset,
                        "query": query,
                    },
                    count=response.hits.total.value,
                ),
                "previous": self._get_previous_page(
                    {
                        "limit": limit,
                        "offset": offset,
                        "query": query,
                    }
                ),
                "results": [
                    {
                        "id": hit.meta.id,
                        "name": hit.name,
                        "country": hit.country,
                        "description": hit.description,
                        "points": hit.points,
                        "price": hit.price,
                        "style": hit.style,
                        "brewery": hit.brewery,
                    }
                    for hit in response
                ],
            }
        )
