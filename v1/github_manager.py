import requests
import os


class GitHubManager:
    """
    This module is responsible for the communication with the GitHub API.
    """

    def __init__(self):
        """
        The constructor that instantiates GitHub Manager.
        """

        self.GITHUB_URL = "https://api.github.com/"
        self.MY_GITHUB_USERNAME = "pavlovab"
        self.personal_github_token = os.environ.get("GITHUB_TOKEN")
        self.authentication = (self.MY_GITHUB_USERNAME, self.personal_github_token)

    def get_user_credentials(self, username):
        """
        Queries the GitHub API and returns the user credentials corresponding to the particular username.
        """

        try:
            response = requests.get(f"{self.GITHUB_URL}users/{username}", auth=self.authentication)
            # response.ok returns True if status_code is less than 400
            if response.ok:
                user_credentials = response.json()
                return user_credentials
            else:
                return "Bad Response!"
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
