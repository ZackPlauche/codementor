import pytest


def test_get_jobs(jobs):
    assert len(jobs) == 15


def test_get_job_details(client, jobs):
    client.get_job_details(jobs[0].random_key)


def test_get_all_jobs(all_jobs):
    assert len(all_jobs) > 15


def test_get_related_jobs(client, all_jobs):
    related_jobs = client.get_jobs(related=True)
    assert len(related_jobs) < len(all_jobs)


def test_get_sessions(client):
    sessions = client.get_sessions()
    assert len(sessions) > 0


def test_get_session_details(client):
    session_details = client.get_session_details(session_id='1434640051')
    assert session_details is not None


def test_get_reviews(client):
    reviews = client.get_reviews()
    assert len(reviews) > 0


def test_get_freelance_jobs(client):
    freelance_jobs = client.get_freelance_jobs()
    assert len(freelance_jobs) > 0
