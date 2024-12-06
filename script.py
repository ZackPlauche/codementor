import codementor

client = codementor.Client.from_env()

reviews = client.get_reviews(username='zackplauche')
from pprint import pprint

print(len(reviews))
import json

with open('reviews.json', 'w') as f:
    json.dump(reviews, f)
