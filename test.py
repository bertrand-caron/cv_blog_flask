from flask import request
import unittest

from application import application, home, cv, blog, contact, data, CONFIG

ROUTES = [home, cv, blog, contact, data]

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.app = application.test_client()

    def tearDown(self):
        pass

    def test_home(self):
        rv = self.app.get('/')

    def test_cv(self):
        rv = self.app.get('/cv')

    def test_blog(self):
        rv = self.app.get('/blog')

    def test_contact(self):
        rv = self.app.get('/contact')

    def test_data(self):
        rv = self.app.get('/data')

if __name__ == '__main__':
    unittest.main()
