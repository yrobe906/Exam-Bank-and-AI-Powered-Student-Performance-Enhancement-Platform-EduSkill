import urllib.request
import json

# Test the POST /api/questions endpoint
url = 'http://localhost:8000/api/questions'

# Test data matching what the frontend might send
test_data = {
    "section_id": 1,
    "question_text": "What is the capital of France?",
    "option_a": "London",
    "option_b": "Paris",
    "option_c": "Berlin",
    "option_d": "Madrid",
    "correct_answer": "B",
    "difficulty": "Easy",
    "marks": 1
}

req = urllib.request.Request(
    url,
    data=json.dumps(test_data).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status: {response.status}")
        print(f"Response: {response.read().decode('utf-8')}")
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code}")
    print(f"Response: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
