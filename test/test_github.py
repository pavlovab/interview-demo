import unittest
from unittest.mock import patch
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from v1.github_manager import GitHubManager


class TestGitHubManager(unittest.TestCase):

    def test_get_user_credentials(self):
        fake_json = {
            "name": "Borislava Borisova",
            "email": "test.email@gmail.com"
        }

        with patch("v1.github_manager.requests.get") as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.json.return_value = fake_json

            manager = GitHubManager()
            user_credentials = manager.get_user_credentials('pavlovab')
            self.assertEqual(user_credentials, fake_json)

            mocked_get.return_value.ok = False

            manager = GitHubManager()
            user_credentials = manager.get_user_credentials('pavlovab')
            self.assertEqual(user_credentials, "Bad Response!")


if __name__ == "__main__":
    unittest.main()
