#!/usr/bin/env python3
"""
Test script to check user profile update functionality.
"""

import requests
import json

# Replace with actual values
BASE_URL = "http://localhost:8000"  # Adjust if different
USERNAME = "fenet"  # Replace with actual username
PASSWORD = "password"  # Replace with actual password

def test_login():
    """Test login and get token."""
    response = requests.post(
        f"{BASE_URL}/api/users/login",
        data={"username_or_email": USERNAME, "password": PASSWORD}
    )
    print(f"Login status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Login response: {data}")
        return data.get("token")
    else:
        print(f"Login failed: {response.text}")
        return None

def test_update_profile(token):
    """Test updating user profile."""
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {
        "full_name": "Updated Name",
        "username": "newusername",  # Test updating username
        "email": "newemail@example.com"
    }

    # Since it's form data, need to send as form
    response = requests.put(
        f"{BASE_URL}/api/users/profile",
        data=update_data,
        headers=headers
    )
    print(f"Update status: {response.status_code}")
    print(f"Update response: {response.text}")

if __name__ == "__main__":
    token = test_login()
    if token:
        test_update_profile(token)