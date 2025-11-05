#!/usr/bin/env python
"""
Script to create a test user for the Load Management System
Run: python create_test_user.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loadproject.settings')
django.setup()

from django.contrib.auth.models import User

# Create test user
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f'User "{username}" already exists!')
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f'Password updated for user "{username}"')
else:
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        is_staff=True,
        is_superuser=True
    )
    print(f'Test user created successfully!')

print(f'\nLogin credentials:')
print(f'Username: {username}')
print(f'Password: {password}')
print(f'\nYou can now login at: http://localhost:8000/auth/login/')
