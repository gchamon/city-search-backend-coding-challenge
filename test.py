import unittest

import backend_lib
from backend import app

KIRK_EXPECTED = sorted([
    {
        "name": "Kirkland",
        "lat": "45.45008",
        "long": "-73.86586"
    },
    {
        "name": "Kirkland Lake",
        "lat": "48.14461",
        "long": "-80.03767"
    },
    {
        "name": "Kirkwood",
        "lat": "38.58339",
        "long": "-90.40678"
    },
    {
        "name": "Kirksville",
        "lat": "40.19475",
        "long": "-92.58325"
    },
    {
        "name": "Kirkland",
        "lat": "47.68149",
        "long": "-122.20874"
    }
], key=lambda x: x["name"])


class TestCatalogLoad(unittest.TestCase):
    def test_load_catalog(self):
        catalog = backend_lib.load_catalog("data/cities_canada-usa.tsv")
        with open("data/cities_canada-usa.tsv") as catalog_fp:
            catalog_lines = len(catalog_fp.readlines())
        self.assertEquals(len(catalog), catalog_lines - 1)


class TestCitySearch(unittest.TestCase):
    def setUp(self):
        self.catalog = backend_lib.load_catalog("data/cities_canada-usa.tsv")

    def test_name_query(self):
        query = "Kirk"
        results = backend_lib.filter_query_results_attributes(backend_lib.query_name(catalog=self.catalog, query=query))
        self.assertEquals(results, KIRK_EXPECTED)

    def test_name_query_empty_result(self):
        query = "Azpilicuetagaraycosaroyarenberecolarrea"
        results = backend_lib.query_name(self.catalog, query=query)
        expected = []
        self.assertEquals(results, expected)

    def test_name_empty_query(self):
        with self.assertRaises(backend_lib.EmptyQueryError):
            query = ""
            backend_lib.query_name(self.catalog, query=query)


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_suggestions_kirk(self):
        response = self.client.get("/suggestions?q=Kirk")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json, KIRK_EXPECTED)

    def test_suggestions_empty_query(self):
        response = self.client.get("/suggestions?q=")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.text, "Empty query q")

    def test_suggestions_missing_city(self):
        response = self.client.get("/suggestions?q=Azpilicuetagaraycosaroyarenberecolarrea")
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.text, "No matches for query 'Azpilicuetagaraycosaroyarenberecolarrea'")


if __name__ == '__main__':
    unittest.main()
