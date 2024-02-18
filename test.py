import unittest
import backend

class TestCatalogLoad(unittest.TestCase):
    def test_load_catalog(self):
        catalog = backend.load_catalog("data/cities_canada-usa.tsv")
        with open("data/cities_canada-usa.tsv") as catalog_fp:
            catalog_lines = len(catalog_fp.readlines())
        self.assertEquals(len(catalog), catalog_lines - 1)

# class TestCitySearch(unittest.TestCase):
#
#     def test_name_query(self):
#         query = "Londo"
#

if __name__ == '__main__':
    unittest.main()