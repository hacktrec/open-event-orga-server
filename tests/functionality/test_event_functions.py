import unittest

from tests.auth_helper import login
from tests.utils import OpenEventTestCase
from tests.setup_database import Setup
from tests.object_mother import ObjectMother
from app import current_app as app
from app.helpers.data import save_to_db


class TestEventFunctions(OpenEventTestCase):
    def setUp(self):
        self.app = Setup.create_app()

    def test_add_event_to_db(self):
        event = ObjectMother.get_event()
        with app.test_request_context():
            save_to_db(event, "Event saved")
            self.assertEqual(event.id, event.id)

if __name__ == '__main__':
    unittest.main()
