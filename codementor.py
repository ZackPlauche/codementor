import os
import time

import requests
from dotenv import load_dotenv

BASE_URL = "https://api.codementor.io/api/v2"

ENDPOINTS = {
    'job detail': '/{random_key}?access_as=mentor',
    'job list': '/requests/search',
}

for key, value in ENDPOINTS.items():
    ENDPOINTS[key] = BASE_URL + value


class Client:

    def __init__(self, access_token: str, refresh_token: str):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Origin": "https://www.codementor.io",
            "Referer": "https://www.codementor.io/",
            "X-Requested-From": "cm-web"
        })
        self.session.cookies.update({
            "ACCESS_TOKEN": access_token,
            "REFRESH_TOKEN": refresh_token
        })

    @classmethod
    def from_env(cls):
        """
        Instantiate the Client using environment variables for access and refresh tokens.

        Returns:
            An instance of the Client class.
        """
        load_dotenv()  # Load environment variables from .env file
        access_token = os.getenv('ACCESS_TOKEN')
        refresh_token = os.getenv('REFRESH_TOKEN')
        return cls(access_token, refresh_token)

    def get_jobs(self, related: bool = False) -> list[dict]:
        """
        Get all available jobs/requests from Codementor by paginating through timestamps

        Args:
            search_type: Type of search ('all' or 'related')

        Returns:
            List of job dictionaries containing all available jobs
        """
        url = ENDPOINTS['job list']
        params = {'search_type': 'all' if not related else 'related'}
        all_jobs = []

        while True:
            try:
                response = self.session.get(url, params=params)

                # Handle rate limiting
                if response.status_code == 429:
                    wait_time = 60  # Default wait time
                    print(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()

                # Process the response
                jobs = response.json()
                if not jobs:
                    break
                all_jobs.extend(jobs)

                # Get timestamp of last job for next request
                last_job = jobs[-1]
                last_timestamp = last_job['created_at']
                params['before_timestamp'] = last_timestamp

                # Add a small delay between requests
                time.sleep(2)

            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                break

        return all_jobs


if __name__ == '__main__':
    client = Client.from_env()
    import json
    with open('jobs.json', 'w') as f:
        json.dump(client.get_jobs(), f)
