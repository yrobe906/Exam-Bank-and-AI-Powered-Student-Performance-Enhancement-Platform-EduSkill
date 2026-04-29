import requests
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

try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
