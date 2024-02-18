import unittest

from backend import app
from test.test_lib import KIRK_EXPECTED


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
