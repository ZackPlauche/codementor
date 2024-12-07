import json
from pathlib import Path

import codementorapi


SAMPLE_OUTPUT_PATH = Path(__file__).parent.parent / 'sample_outputs'
SAMPLE_OUTPUT_PATH.mkdir(exist_ok=True)

codementor = codementorapi.Client.from_env()


def save_to_json(data: dict | list[dict] | list[str], filename: str):
    with open(SAMPLE_OUTPUT_PATH / f'{filename}.json', 'w') as f:
        json.dump(data, f)


jobs = codementor.get_jobs()
save_to_json(jobs, 'jobs')

# Define stuff for the rest of the job.
job = jobs[0]

user = job['user']
first_name = user['name'].split(' ')[0]
message = f'Hey {first_name}!\n\nI\'d love to help you with this. 🙂\n\nWould you like to have a call?'

job_details = codementor.get_job_details(job_id=job['random_key'])
save_to_json(job_details, 'job_details')

job_interest_response = codementor.send_job_interest(
    job_id=job['random_key'], message=message)
save_to_json(job_interest_response, 'job_interest_response')

send_message_response = codementor.send_message(username=user['username'], message=message)
save_to_json(send_message_response, 'send_message_response')

reviews = codementor.get_reviews()
save_to_json(reviews, 'reviews')

sessions = codementor.get_sessions()
save_to_json(sessions, 'sessions')

freelance_jobs = codementor.get_freelance_jobs()
save_to_json(freelance_jobs, 'freelance_jobs')
