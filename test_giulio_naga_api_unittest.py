import unittest
from giulio_naga_api import app

class FlaskTestCase(unittest.TestCase):
    
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<table", response.data)

    def test_pagination(self):
        response = self.client.get("/?offset=10&limit=5")
        self.assertEqual(response.status_code, 200) 
        self.assertIn(b"<table", response.data) 

    def test_intern_endpoint(self):
        response = self.client.get("/intern")
        self.assertEqual(response.status_code, 200) 
        self.assertIsInstance(response.json, dict) 

    def test_not_found(self):
        response = self.client.get("/does_not_exist")
        self.assertEqual(response.status_code, 404)
