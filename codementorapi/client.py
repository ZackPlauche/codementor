import os
import time
from typing import Any, Optional

import requests
from dotenv import load_dotenv

from .models import (
    JobListResponse,
    JobListItem,
    JobDetailResponse,
    Review,
    ReviewListResponse,
    MessageResponse,
    SessionListItem,
    SessionDetailResponse,
    SessionListResponse,
    FreelanceJobListResponse,
    FreelanceJobListItem
)

BASE_URL = "https://api.codementor.io/api/v2"

ENDPOINTS = {
    'job detail': '/requests/{random_key}?access_as=mentor',
    'job list': '/requests/search',
    'job apply': '/requests/{random_key}/interests',
    'user chat': '/chats/messages/{username}',
    'session list': '/lessons',
    'session detail': '/lessons/{session_id}',
    'reviews': '/users/{username}/reviews',
    'me': '/me',
    'freelance jobs': '/offline-helps',
}

# Add base URL to all endpoints
ENDPOINTS = {k: BASE_URL + v for k, v in ENDPOINTS.items()}


class Client:
    """A client for interacting with the Codementor API.

    This client handles authentication and provides methods for accessing various
    Codementor API endpoints including jobs, sessions, reviews and more.

    Args:
        access_token (str): The Codementor API access token
        refresh_token (str): The Codementor API refresh token

    Example:
        >>> client = Client(access_token="abc123", refresh_token="xyz789")
        >>> jobs = client.get_jobs()
    """

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
        """Instantiate the Client using environment variables."""
        load_dotenv(override=True)
        return cls(
            access_token=os.getenv('CODEMENTOR_ACCESS_TOKEN'),
            refresh_token=os.getenv('CODEMENTOR_REFRESH_TOKEN')
        )

    def _paginate(
        self,
        url: str,
        params: dict[str, Any] = None,
        timestamp_key: str = 'before_timestamp',
        created_at_key: str = 'created_at'
    ) -> list[dict]:
        """Generic pagination method for endpoints that use timestamp-based pagination."""
        params = params or {}
        all_items = []

        while True:
            try:
                response = self._make_request('get', url, params=params)
                items = response.json()

                if not items:
                    break

                all_items.extend(items)

                # Update timestamp for next page
                last_item = items[-1]
                params[timestamp_key] = last_item[created_at_key]

                time.sleep(2)  # Rate limiting delay

            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                break

        return all_items

    def _make_request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> requests.Response:
        """Make an HTTP request with rate limit handling."""
        while True:
            response = self.session.request(method, url, **kwargs)

            if response.status_code == 429:
                wait_time = 60
                print(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            return response

    def get_jobs(self, related: bool = False, all: bool = False) -> JobListResponse:
        """Get jobs/requests from Codementor."""
        params = {'search_type': 'all' if not related else 'related'}

        if all:
            jobs = self._paginate(ENDPOINTS['job list'], params)
        else:
            response = self._make_request(
                'get', ENDPOINTS['job list'], params=params)
            jobs = response.json()
        return [JobListItem.model_validate(job) for job in jobs]

    def get_job_details(self, job_random_key: str) -> JobDetailResponse:
        """Get details for a specific job."""
        url = ENDPOINTS['job detail'].format(random_key=job_random_key)
        response = self._make_request('get', url)
        return JobDetailResponse.model_validate(response.json())

    def send_job_interest(
        self,
        job_random_key: str,
        message: str,
        open_to_special_rate: bool = False
    ) -> dict:
        """Send interest in a job posting."""
        url = ENDPOINTS['job apply'].format(random_key=job_random_key)
        payload = {
            'message': message,
            'open_to_special_rate': open_to_special_rate
        }
        response = self._make_request('post', url, json=payload)
        return response.json()

    def send_message(self, username: str, message: str) -> MessageResponse:
        """Send a chat message to a user."""
        url = ENDPOINTS['user chat'].format(username=username)
        payload = {
            'message': {
                'content': message,
                'request': {'temp_message_id': None},
                'type': 'message',
            }
        }
        response = self._make_request('post', url, json=payload)
        return MessageResponse.model_validate(response.json())

    def get_sessions(self) -> SessionListResponse:
        """Get all sessions."""
        sessions = self._paginate(ENDPOINTS['session list'])
        return [SessionListItem.model_validate(session) for session in sessions]

    def get_session_details(self, session_id: str) -> SessionDetailResponse:
        """Get details for a specific session."""
        url = ENDPOINTS['session detail'].format(session_id=session_id)
        response = self._make_request('get', url)
        return SessionDetailResponse.model_validate(response.json())

    def get_reviews(self, username: Optional[str] = None) -> ReviewListResponse:
        """Get all reviews for a user."""
        if username is None:
            response = self._make_request('get', ENDPOINTS['me'])
            username = response.json()['username']

        url = ENDPOINTS['reviews'].format(username=username)
        return [Review.model_validate(review) for review in self._paginate(url)]

    def get_freelance_jobs(self) -> FreelanceJobListResponse:
        """Get all freelance jobs."""
        jobs = self._paginate(
            ENDPOINTS['freelance jobs'],
            params={'type': 'solved'},
            timestamp_key='offset'
        )
        return [FreelanceJobListItem.model_validate(job) for job in jobs]
