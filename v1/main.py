# Author Borislava Borisova
# A command-line Python program, which retrieves the information of a GitHub User and creates a new Contact or updates
# an existing contact in Freshdesk.

from github_manager import GitHubManager
from freshdesk_manager import FreshdeskManager
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", type=str, help="The username of the person to become a new contact in Freshdesk.")
    parser.add_argument("subdomain", type=str, help="The Freshdesk subdomain used to create a new Contact or update an\
                    existing one.")
    args = parser.parse_args()

    # Get GitHub User credentials to work with.
    github_communication = GitHubManager()
    user_data = github_communication.get_user_credentials(args.username)

    # Create a new Contact or update an existing one.
    freshdesk = FreshdeskManager(args.subdomain)
    response = freshdesk.add_contact(user_data)
    print(response)


if __name__ == "__main__":
    main()
