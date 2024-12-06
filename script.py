import codementor

client = codementor.Client.from_env()

response_data = client.get_freelance_jobs()
print(len(response_data))
import json

with open('response_data.json', 'w') as f:
    json.dump(response_data, f)
