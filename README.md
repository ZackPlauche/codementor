# Codementor API

A Python client for accessing Codementor's internal API. Use it to get data about new jobs, previous jobs and sessions, and reviews.

```python
import codementor


client = codementor.Client(
    access_token='<your access token>',
    refresh_token='<your refresh token>',
)

# or

client = codementor.Client.from_env()

# Get latest available jobs (unfiltered)
jobs = client.get_jobs()

# Get all available jobs (unfiltered)
jobs = client.get_jobs(all=True)

# Get related available jobs
related_jobs = client.get_related_jobs(related=True)

# Get all related available jobs
related_jobs = client.get_related_jobs(related=True, all=True)

# Get job details.
job_details = client.get_job_details(job_id=jobs[0]['random_id'])

# Get job details.
sessions = client.get_sessions()
session_details = client.get_session_details(sessions[0]['id'])
reviews = client.get_reviews()
freelance_jobs = client.get_freelance_jobs()
```
