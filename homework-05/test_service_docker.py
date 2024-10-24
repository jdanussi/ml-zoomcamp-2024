import requests
import json


customer = {
    'job': 'management',
    'duration': 400,
    'poutcome': 'success'
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=customer)
result = response.json()

print(json.dumps(result, indent=2))