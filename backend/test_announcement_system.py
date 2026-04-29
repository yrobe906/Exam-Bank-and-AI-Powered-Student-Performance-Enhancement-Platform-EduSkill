#!/usr/bin/env python3
"""
Complete test script for the Announcement System
Run this to verify the system works correctly
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

def login_user(username, password):
    """Login and get JWT token"""
    response = requests.post(
        f'{BASE_URL}/api/users/login',
        data={'username_or_email': username, 'password': password}
    )

    if response.status_code == 200:
        data = response.json()
        if 'token' in data:
            print(f'✅ Login successful for {username}')
            return data['token']
        else:
            print(f'❌ Login failed: {data}')
    else:
        print(f'❌ Login request failed: {response.status_code} - {response.text}')

    return None

def test_get_announcements(token, role=None):
    """Test GET announcements"""
    headers = {'Authorization': f'Bearer {token}'}
    url = f'{BASE_URL}/api/announcements/'
    if role:
        url += f'?role={role}'

    response = requests.get(url, headers=headers)
    print(f'GET announcements ({role or "all"}) - Status: {response.status_code}')

    if response.status_code == 200:
        data = response.json()
        print(f'✅ Retrieved {len(data)} announcements')
        return True
    else:
        print(f'❌ Failed: {response.text}')
        return False

def test_create_announcement(token):
    """Test POST announcement (requires eduoffice/admin)"""
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'title': 'Test Announcement',
        'message': 'This is a test announcement created via API',
        'category': 'academic',
        'target_role': 'student'
    }

    response = requests.post(
        f'{BASE_URL}/api/announcements/',
        json=data,
        headers=headers
    )

    print(f'POST announcement - Status: {response.status_code}')

    if response.status_code == 200:
        result = response.json()
        print(f'✅ Announcement created: {result["title"]}')
        return result['id']
    else:
        print(f'❌ Failed: {response.text}')
        return None

def main():
    print('🧪 Testing Announcement System')
    print('=' * 50)

    # Test 1: Login as student and try to read announcements
    print('\n1. Testing Student Access:')
    student_token = login_user('fenet', 'password')  # Use actual password
    if student_token:
        test_get_announcements(student_token, 'student')

    # Test 2: Login as teacher and try to read announcements
    print('\n2. Testing Teacher Access:')
    teacher_token = login_user('rial', 'password')  # Use actual password
    if teacher_token:
        test_get_announcements(teacher_token, 'teacher')

    # Test 3: Login as eduoffice and test full access
    print('\n3. Testing EduOffice Access:')
    eduoffice_token = login_user('amana', 'password')  # Use actual password
    if eduoffice_token:
        # Test reading
        test_get_announcements(eduoffice_token)

        # Test creating
        announcement_id = test_create_announcement(eduoffice_token)

        if announcement_id:
            print(f'\n✅ Created announcement with ID: {announcement_id}')

    # Test 4: Try to create as student (should fail)
    print('\n4. Testing Student Create Access (should fail):')
    if student_token:
        test_create_announcement(student_token)

    print('\n' + '=' * 50)
    print('🎉 Testing completed!')
    print('\nNote: Update passwords in this script with actual user passwords')

if __name__ == '__main__':
    main()