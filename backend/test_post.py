import urllib.request
import json

# Test creating an exam with pricing
url = 'http://localhost:8000/api/exams'
data = {
    "name": "Premium Test Exam",
    "sector_id": 2,
    "total_questions": 10,
    "duration": 30,
    "total_marks": 100,
    "exam_type": "Model",
    "pricing_type": "Premium",
    "amount": 50.0
}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode('utf-8'),
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
