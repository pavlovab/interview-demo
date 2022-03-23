import requests
import os


class FreshdeskManager:
    """
        This module is responsible for the communication with the GitHub API.
    """

    def __init__(self, subdomain):
        """
        The constructor that instantiates Freshdesk Manager.
        """

        self.freshdesk_URL = f"https://{subdomain}.freshdesk.com/api/v2/"
        self.freshdesk_token = os.environ.get("FRESHDESK_TOKEN")
        self.headers = {
            "Authorization": self.freshdesk_token,
        }

    def get_all_contacts(self):
        """
        Queries the Freshdesk API and returns a list of all the Contacts.
        """

        try:
            response = requests.get(f"{self.freshdesk_URL}contacts", headers=self.headers)
            if response.ok:
                all_contacts = response.json()
                return all_contacts
            else:
                return "Bad Response!"
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    def add_contact(self, user_credentials):
        """
        Creates a new Contact at the domain, given the necessary user credentials.
        Checks if the Contact already exists. If it does - updates the Contact instead.
        """

        all_contacts = self.get_all_contacts()
        for contact in all_contacts:
            if contact['unique_external_id'] == str(user_credentials['id']):
                print("Contact already exists! Updating contact...")
                return self.update_contact_info(contact['id'], user_credentials)

        contact_data = {
            'unique_external_id': str(user_credentials['id']),
        }
        if user_credentials['name']:
            contact_data['name'] = user_credentials['name']
        else:
            return "Name field is mandatory!"
        if user_credentials['email']:
            contact_data['email'] = user_credentials['email']
        if user_credentials['twitter_username']:
            contact_data['twitter_id'] = user_credentials['twitter_username']
        if user_credentials['bio']:
            contact_data['description'] = user_credentials['bio']
        if user_credentials['location']:
            contact_data['address'] = user_credentials['location']

        try:
            response = requests.post(f"{self.freshdesk_URL}contacts", headers=self.headers, json=contact_data)
            if response.ok:
                return "New contact has been added!"
            else:
                return "Bad Response!"
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    def update_contact_info(self, user_id, user_credentials):
        """
        Updates the contact info via user_id of an already existing Contact. The new user info is provided by
        user_credentials.
        """

        github_fields = ["name", "email", "twitter_username", "bio", "location"]
        freshdesk_fields = ["name", "email", "twitter_id", "description", "address"]
        contact_data = {}
        for n in range(len(github_fields)):
            try:
                data = user_credentials[github_fields[n]]
            except KeyError:
                continue
            else:
                contact_data[freshdesk_fields[n]] = data

        try:
            response = requests.put(f"{self.freshdesk_URL}contacts/{user_id}", headers=self.headers, json=contact_data)
            if response.ok:
                return "Contact updated!"
            else:
                return "Bad Response!"
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
