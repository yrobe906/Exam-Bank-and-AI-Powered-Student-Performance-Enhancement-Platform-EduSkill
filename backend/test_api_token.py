# Test script to directly test the API endpoint with a token
import json
import requests

# First, login to get a token
login_data = {
    "username_or_email": "tade",
    "password": "123456"  # Use actual password
}

login_response = requests.post("http://127.0.0.1:8000/api/users/login", data=login_data)
print(f"Login response status: {login_response.status_code}")
print(f"Login response: {login_response.json()}")

if login_response.status_code == 200:
    token = login_response.json()["token"]
    
    # Now test the student-performance endpoint
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get("http://127.0.0.1:8000/api/users/teacher/student-performance", headers=headers)
    print(f"\nStudent performance response status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
else:
    print("Login failed!")

