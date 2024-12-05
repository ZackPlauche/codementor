import os
import time

import requests
from dotenv import load_dotenv

BASE_URL = "https://api.codementor.io/api/v2"

ENDPOINTS = {
    'job detail': '/requests/{random_key}?access_as=mentor',
    'job list': '/requests/search',
    'job apply': '/requests/{random_key}/interests',
    'user chat': '/chats/messages/{username}',
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

    def get_jobs(self, related: bool = False, all: bool = False) -> list[dict]:
        """
        Get jobs/requests from Codementor, optionally paginating through all available jobs

        Args:
            related: Whether to get related jobs only
            all: Whether to get all available jobs by paginating through timestamps

        Returns:
            List of job dictionaries
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

                # If not getting all jobs, return after first batch
                if not all:
                    break

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

    def _get_job_detail(self, job_id: str):
        url = ENDPOINTS['job detail'].format(random_key=job_id)
        response = self.session.get(url)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()

    def _send_job_interest(self, job_id: str, message: str, open_to_special_rate: bool = False):
        """
        Send interest in a job posting to Codementor.

        Args:
            job_id: The ID of the job to apply for
            message: Cover letter message to send with application
            open_to_special_rate: Whether to accept special rate requests

        Returns:
            dict: Response data from the API

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = ENDPOINTS['job apply'].format(random_key=job_id)
        payload = {
            'message': message,
            'open_to_special_rate': open_to_special_rate
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()

    def message_user(self, username: str, message: str):
        url = ENDPOINTS['user chat'].format(username=username)


if __name__ == '__main__':
    client = Client.from_env()
    import json
    with open('jobs.json', 'w') as f:
        json.dump(client.get_jobs(), f)
