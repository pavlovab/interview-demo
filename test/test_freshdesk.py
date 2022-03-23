import unittest
from unittest.mock import patch
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from v1.freshdesk_manager import FreshdeskManager


class TestFreshdeskManager(unittest.TestCase):

    def setUp(self):
        self.fake_credentials = {
            'id': '1',
            'unique_external_id': "0152",
            'name': 'Kori Jorgens',
            'email': None,
            'twitter_username': None,
            'bio': None,
            'location': None
        }

        self.fake_json = [
            {
                "name": "Borislava Borisova",
                "email": "test.email@gmail.com"
            },
            {
                "name": "Gergana Jordanova",
                "twitter_id": "gergana.test"
            }
        ]

        self.fake_credentials_without_name = {
            'id': '1',
            'unique_external_id': "0152",
            'name': None,
            'email': None,
            'twitter_username': None,
            'bio': None,
            'location': None
        }

    def test_get_all_contacts(self):
        with patch("v1.freshdesk_manager.requests.get") as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.json.return_value = self.fake_json

            manager = FreshdeskManager('pavlova-demo')
            all_contacts = manager.get_all_contacts()
            self.assertEqual(all_contacts, self.fake_json)

            mocked_get.return_value.ok = False

            manager = FreshdeskManager('pavlova-demo')
            all_contacts = manager.get_all_contacts()
            self.assertEqual(all_contacts, "Bad Response!")

    def test_add_contact(self):
        with patch("v1.freshdesk_manager.requests.post") as mocked_post:
            mocked_post.return_value.ok = True

            manager = FreshdeskManager('pavlova-demo')
            status = manager.add_contact(self.fake_credentials)
            self.assertEqual(status, "New contact has been added!")

            mocked_post.return_value.ok = False

            manager = FreshdeskManager('pavlova-demo')
            status = manager.add_contact(self.fake_credentials)
            self.assertEqual(status, "Bad Response!")

            status = manager.add_contact(self.fake_credentials_without_name)
            self.assertEqual(status, "Name field is mandatory!")

    def test_update_contact_info(self):
        with patch("v1.freshdesk_manager.requests.put") as mocked_put:
            mocked_put.return_value.ok = True

            manager = FreshdeskManager('pavlova-demo')
            status = manager.update_contact_info(1, self.fake_credentials)
            self.assertEqual(status, "Contact updated!")

            mocked_put.return_value.ok = False

            manager = FreshdeskManager('pavlova-demo')
            status = manager.update_contact_info(1, self.fake_credentials)
            self.assertEqual(status, "Bad Response!")


if __name__ == "__main__":
    unittest.main()
