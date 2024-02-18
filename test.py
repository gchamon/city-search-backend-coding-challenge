import unittest

import backend


class TestCatalogLoad(unittest.TestCase):
    def test_load_catalog(self):
        catalog = backend.load_catalog("data/cities_canada-usa.tsv")
        with open("data/cities_canada-usa.tsv") as catalog_fp:
            catalog_lines = len(catalog_fp.readlines())
        self.assertEquals(len(catalog), catalog_lines - 1)


class TestCitySearch(unittest.TestCase):
    def setUp(self):
        self.catalog = backend.load_catalog("data/cities_canada-usa.tsv")

    def test_name_query(self):
        query = "Kirk"
        results = backend.query_name(catalog=self.catalog, query=query)
        expected = [
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
        ]
        self.assertEquals(results, expected)


if __name__ == '__main__':
    unittest.main()
