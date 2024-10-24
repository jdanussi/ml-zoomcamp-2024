import requests
import json


customer = {
    'job': 'student',
    'duration': 280,
    'poutcome': 'failure'
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=customer)
result = response.json()

print(json.dumps(result, indent=2))