from django.core.management.base import BaseCommand

from elasticsearch_dsl import connections
from elasticsearch.helpers import bulk

from catalog.constants import ES_INDEX
from catalog.models import Beer


class Command(BaseCommand):
    help = "Updates the Elasticsearch index."

    # changed
    def _document_generator(self):
        for beer in Beer.objects.iterator():
            yield {
                "_index": ES_INDEX,
                "_id": beer.id,
                "name": beer.name,
                "style": beer.style,
                "country": beer.country,
                "price": beer.price,
                "brewery": beer.brewery,
                "description": beer.description,
                "points": beer.points,
            }

    # changed
    def handle(self, *args, **kwargs):
        self.stdout.write(f'Bulk updating documents on "{ES_INDEX}" index...')
        connection = connections.get_connection()
        succeeded, _ = bulk(
            connection, actions=self._document_generator(), stats_only=True
        )
        self.stdout.write(f'Updated {succeeded} documents on "{ES_INDEX}" successfully')
