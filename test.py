from typing import Any
import unittest

from application import APPLICATION, home, cv, blog, contact, data

ROUTES = [home, cv, blog, contact, data]

def validate_answer(answer: Any) -> None:
    if answer.status != '200 OK':
        raise AssertionError()

class TestIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.app = APPLICATION.test_client()

    def tearDown(self) -> None:
        pass

    def test_home(self) -> None:
        validate_answer(self.app.get('/'))

    def test_cv(self) -> None:
        validate_answer(self.app.get('/cv'))

    def test_blog(self) -> None:
        validate_answer(self.app.get('/blog'))

    def test_contact(self) -> None:
        validate_answer(self.app.get('/contact'))

    def test_data(self) -> None:
        validate_answer(self.app.get('/data'))

if __name__ == '__main__':
    unittest.main()
