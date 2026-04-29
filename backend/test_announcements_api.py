#!/usr/bin/env python3
"""
Test script for the announcements API.
Make sure the server is running before executing this.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_announcement(token):
    """Test creating an announcement."""
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "Test Announcement",
        "message": "This is a test announcement for students.",
        "category": "academic",
        "target_role": "student"
    }

    response = requests.post(f"{BASE_URL}/api/announcements/", json=data, headers=headers)
    print(f"Create Announcement - Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Announcement created successfully!")
        return response.json()
    else:
        print(f"❌ Failed to create announcement: {response.text}")
        return None

def test_get_announcements(role=None):
    """Test getting announcements."""
    url = f"{BASE_URL}/api/announcements/"
    if role:
        url += f"?role={role}"

    response = requests.get(url)
    print(f"Get Announcements ({role or 'all'}) - Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {len(data)} announcements")
        return data
    else:
        print(f"❌ Failed to get announcements: {response.text}")
        return []

def test_update_announcement(token, announcement_id):
    """Test updating an announcement."""
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "Updated Test Announcement",
        "message": "This announcement has been updated."
    }

    response = requests.put(f"{BASE_URL}/api/announcements/{announcement_id}", json=data, headers=headers)
    print(f"Update Announcement - Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Announcement updated successfully!")
        return response.json()
    else:
        print(f"❌ Failed to update announcement: {response.text}")
        return None

def test_delete_announcement(token, announcement_id):
    """Test deleting an announcement."""
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.delete(f"{BASE_URL}/api/announcements/{announcement_id}", headers=headers)
    print(f"Delete Announcement - Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Announcement deleted successfully!")
        return True
    else:
        print(f"❌ Failed to delete announcement: {response.text}")
        return False

def main():
    # Note: You need to get a valid token from an eduoffice/admin user
    # For testing, replace this with a real token
    token = "your_jwt_token_here"

    print("🧪 Testing Announcements API")
    print("=" * 50)

    # Test getting announcements (should work without auth for reading)
    print("\n1. Testing GET announcements...")
    announcements = test_get_announcements()
    student_announcements = test_get_announcements("student")
    teacher_announcements = test_get_announcements("teacher")

    if not token or token == "your_jwt_token_here":
        print("\n⚠️  Skipping authenticated tests - please provide a valid JWT token")
        return

    # Test creating an announcement
    print("\n2. Testing POST announcement...")
    created = test_create_announcement(token)
    if created:
        announcement_id = created['id']

        # Test updating
        print("\n3. Testing PUT announcement...")
        test_update_announcement(token, announcement_id)

        # Test deleting
        print("\n4. Testing DELETE announcement...")
        test_delete_announcement(token, announcement_id)

    print("\n🎉 API testing completed!")

if __name__ == "__main__":
    main()