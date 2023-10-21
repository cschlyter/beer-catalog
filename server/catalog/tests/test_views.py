from rest_framework.test import APIClient, APITestCase
import uuid
import json
import pathlib
from unittest.mock import patch
from django.conf import settings
from elasticsearch_dsl import connections
from catalog.constants import ES_MAPPING
from catalog.models import Beer
from catalog.serializers import BeerSerializer


class ViewTests(APITestCase):
    fixtures = ["test_beers.json"]

    def setUp(self):
        self.client = APIClient()

    def test_empty_query_returns_everything(self):
        response = self.client.get("/api/v1/catalog/beers/")
        beers = Beer.objects.all()
        results_data = response.data.get("results")
        self.assertJSONEqual(
            json.dumps(results_data), BeerSerializer(beers, many=True).data
        )

    def test_query_matches_style(self):
        response = self.client.get(
            "/api/v1/catalog/beers/",
            {
                "query": "Stout",
            },
        )
        results = response.data.get("results")
        self.assertEquals(1, len(results))
        self.assertEquals(
            "bc13d35f-3da3-4e95-8ca0-d4442c83c42a",
            results[0]["id"],
        )

    def test_query_matches_brewery(self):
        response = self.client.get(
            "/api/v1/catalog/beers/",
            {
                "query": "Scarlet",
            },
        )
        results = response.data.get("results")
        self.assertEquals(1, len(results))
        self.assertEquals(
            "a7c3811d-7cc3-45f0-9584-6f50d87f76ce",
            results[0]["id"],
        )

    def test_query_matches_description(self):
        response = self.client.get(
            "/api/v1/catalog/beers/",
            {
                "query": "beer",
            },
        )
        results = response.data.get("results")
        self.assertEquals(4, len(results))
        self.assertCountEqual(
            [
                "bc13d35f-3da3-4e95-8ca0-d4442c83c42a",
                "a7c3811d-7cc3-45f0-9584-6f50d87f76ce",
                "7524846b-ba3c-43b2-b516-03c43a53851a",
                "63362025-82cd-46e6-a105-13fcb2d0f46a",
            ],
            [item["id"] for item in results],
        )

    def test_can_filter_on_country(self):
        response = self.client.get(
            "/api/v1/catalog/beers/",
            {
                "country": "Rivia",
            },
        )
        results = response.data.get("results")
        self.assertEquals(2, len(results))
        self.assertCountEqual(
            [
                "7524846b-ba3c-43b2-b516-03c43a53851a",
                "63362025-82cd-46e6-a105-13fcb2d0f46a",
            ],
            [item["id"] for item in results],
        )

    def test_can_filter_on_points(self):
        response = self.client.get(
            "/api/v1/catalog/beers/",
            {
                "points": 87,
            },
        )
        results = response.data.get("results")
        self.assertEquals(1, len(results))
        self.assertEquals(
            "a7c3811d-7cc3-45f0-9584-6f50d87f76ce",
            results[0]["id"],
        )

    def test_country_must_be_exact_match(self):
        response = self.client.get(
            "/api/v1/catalog/beers/",
            {
                "country": "Rivias",
            },
        )
        results = response.data.get("results")
        self.assertEquals(0, len(results))
        self.assertJSONEqual(json.dumps(results), [])

    def test_search_can_be_paginated(self):
        response = self.client.get(
            "/api/v1/catalog/beers/",
            {
                "limit": 1,
                "offset": 1,
            },
        )
        # Count is equal to total number of results in database
        # We're loading 3 beers into the database via fixtures
        self.assertEqual(4, response.data["count"])
        self.assertEqual(1, len(response.data["results"]))
        self.assertIsNotNone(response.data["previous"])
        self.assertIsNotNone(response.data["next"])

    def test_search_results_returned_in_correct_order(self):
        response = self.client.get(
            "/api/v1/catalog/beers/",
            {
                "query": "Amber",
            },
        )

        results = response.data.get("results")
        self.assertEquals(2, len(results))
        self.assertListEqual(
            [
                "63362025-82cd-46e6-a105-13fcb2d0f46a",
                "7524846b-ba3c-43b2-b516-03c43a53851a",
            ],
            [item["id"] for item in results],
        )


class ESViewTests(APITestCase):
    def setUp(self):
        self.index = f"test-beer-{uuid.uuid4()}"
        self.connection = connections.get_connection()
        self.connection.indices.create(
            index=self.index,
            body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0,
                },
                "mappings": ES_MAPPING,
            },
        )

        # Load fixture data
        fixture_path = pathlib.Path(
            settings.BASE_DIR / "catalog" / "fixtures" / "test_beers.json"
        )
        with open(fixture_path, "rt") as fixture_file:
            fixture_data = json.loads(fixture_file.read())
            for beer in fixture_data:
                fields = beer["fields"]
                self.connection.create(
                    index=self.index,
                    id=fields["id"],
                    body={
                        "name": fields["name"],
                        "country": fields["country"],
                        "description": fields["description"],
                        "points": fields["points"],
                        "price": fields["price"],
                        "style": fields["style"],
                        "brewery": fields["brewery"],
                    },
                    refresh=True,
                )

    def test_query_matches_style(self):
        with patch("catalog.views.constants") as mock_constants:
            mock_constants.ES_INDEX = self.index
            response = self.client.get(
                "/api/v1/catalog/es-beers/",
                {
                    "query": "Stout",
                },
            )
            results = response.data["results"]
        self.assertEquals(1, len(results))
        self.assertEquals("bc13d35f-3da3-4e95-8ca0-d4442c83c42a", results[0]["id"])

    def tearDown(self):
        self.connection.indices.delete(index=self.index)
