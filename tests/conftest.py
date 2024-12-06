import pytest
import codementor


@pytest.fixture
def client():
    """Create a Codementor client instance from environment variables."""
    return codementor.Client.from_env()


@pytest.fixture
def jobs(client) -> list[dict]:
    """Get a list of current jobs."""
    return client.get_jobs()


@pytest.fixture
def all_jobs(client) -> list[dict]:
    """Get a list of all available jobs."""
    jobs = client.get_jobs(all=True)
    print('There were this many jobs:', len(jobs))
    return jobs
