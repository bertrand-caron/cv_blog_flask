from typing import Any
import unittest

from application import APPLICATION, home, cv, blog, contact, data
from helpers.db import create_tables
from helpers.bootstrap import icon_tag
from helpers.sections import img_url_for

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

    def test_db(self) -> None: # pylint: disable=no-self-use
        create_tables()
        img_url_for('http://test.com/a.png')
        img_url_for('')

    def test_helpers(self) -> None: # pylint: disable=no-self-use
        icon_tag('')

    def test_validate_answer_works(self) -> None:
        try:
            validate_answer(self.app.get('/null'))
            raise Exception('This should not have been triggered.')
        except AssertionError:
            return None

if __name__ == '__main__':
    unittest.main()
