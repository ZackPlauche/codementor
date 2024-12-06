import pytest
import codementor


@pytest.fixture
def client():
    return codementor.Client.from_env()


@pytest.fixture
def jobs(client) -> list[dict]:
    return client.get_jobs()


def test_get_jobs(jobs):
    assert len(jobs) == 15


def test_get_job_details(client, jobs):
    client._get_job_detail(jobs[0]['random_key'])


@pytest.fixture
def all_jobs(client) -> list[dict]:
    jobs = client.get_jobs(all=True)
    print('There were this many jobs:', len(jobs))
    return jobs


def test_get_all_jobs(all_jobs):
    assert len(all_jobs) > 15


def test_get_related_jobs(client, all_jobs):
    related_jobs = client.get_jobs(related=True)
    assert len(related_jobs) < len(all_jobs)
    
    
def test_get_sessions(client):
    sessions = client.get_sessions()
    assert len(sessions) > 0