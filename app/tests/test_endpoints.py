
#!/usr/bin/env python3
"""Testing all main endpoints with pytest fixtures."""

import httpx
import base64
from typing import Dict
import pytest


# Configuration
BASE_URL = "http://0.0.0.0:8000"
TEST_USER = "test_user"
TEST_PASSWORD = "test_pass"


@pytest.fixture
def auth_headers() -> Dict[str, str]:
    """Create basic auth headers."""
    credentials = f"{TEST_USER}:{TEST_PASSWORD}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded}"}


@pytest.fixture
def client():
    """HTTP client fixture."""
    return httpx.Client()


@pytest.fixture
def test_user(client):
    """Create test user and return credentials."""
    user_data = {"username": TEST_USER, "password": TEST_PASSWORD}
    response = client.post(f"{BASE_URL}/api/users/", json=user_data)
    
    # User might already exist, check for both success and conflict
    if response.status_code == 201:
        data = response.json()
        assert data["username"] == TEST_USER
        print("Test user created")
    elif response.status_code == 400 and "already registered" in response.json().get("detail", ""):
        print("Test user already exists")
    else:
        raise Exception(f"Unexpected response: {response.status_code} - {response.text}")
    
    return {"username": TEST_USER, "password": TEST_PASSWORD}


@pytest.fixture
def test_link(client, auth_headers):
    """Create test link and return its data."""
    link_data = {
        "original_url": "https://www.example.com",
        "expires_in_days": 7
    }
    response = client.post(f"{BASE_URL}/api/links/", json=link_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["original_url"] == "https://www.example.com"
    assert "short_url" in data
    return data


def test_basic_endpoints(client):
    """Test basic application endpoints."""
    print("Testing basic endpoints...")
    
    # Test root endpoint
    response = client.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "URL Alias Service"
    print("Root endpoint works")
    
    # Test health endpoint
    response = client.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("Health endpoint works")


def test_user_endpoints(client, test_user):
    """Test user management endpoints."""
    print("\nTesting user endpoints...")
    # test_user fixture already handles user creation
    assert test_user["username"] == TEST_USER
    print("User creation works")


def test_link_creation(client, auth_headers, test_user):
    """Test link creation."""
    print("\nTesting link creation...")
    
    link_data = {
        "original_url": "https://www.example.com/create",
        "expires_in_days": 7
    }
    response = client.post(f"{BASE_URL}/api/links/", json=link_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["original_url"] == "https://www.example.com/create"
    assert "short_url" in data
    print("Link creation works")


def test_link_listing(client, auth_headers, test_link):
    """Test link listing."""
    print("\nTesting link listing...")
    
    response = client.get(f"{BASE_URL}/api/links/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)
    print("Link listing works")


def test_get_specific_link(client, auth_headers, test_link):
    """Test getting specific link."""
    print("\nTesting get specific link...")
    
    short_url = test_link["short_url"]
    response = client.get(f"{BASE_URL}/api/links/{short_url}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["short_url"] == short_url
    print("Get specific link works")


def test_link_update(client, auth_headers, test_link):
    """Test link update."""
    print("\nTesting link update...")
    
    short_url = test_link["short_url"]
    update_data = {"is_active": False}
    response = client.put(f"{BASE_URL}/api/links/{short_url}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] is False
    print("Link update works")


def test_stats_endpoints(client, auth_headers, test_user):
    """Test statistics endpoints."""
    print("\nTesting stats endpoints...")
    
    response = client.get(f"{BASE_URL}/api/stats/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    print("Get all stats works")


def test_redirect_endpoint(client):
    """Test redirect functionality."""
    print("\nTesting redirect endpoint...")
    
    # Test redirect with non-existent URL
    response = client.get(f"{BASE_URL}/nonexistent", follow_redirects=False)
    # Should return 404 for non-existent link
    assert response.status_code == 404
    print("Redirect endpoint works (correctly returns 404 for non-existent link)")


def test_authentication_unauthorized(client):
    """Test unauthorized access to protected endpoints."""
    print("\nTesting authentication...")
    
    # Test unauthorized access to protected endpoints
    link_data = {"original_url": "https://www.example.com"}
    response = client.post(f"{BASE_URL}/api/links/", json=link_data)
    assert response.status_code == 401
    print("Authentication protection works")


def test_authentication_invalid_credentials(client):
    """Test invalid credentials."""
    print("\nTesting invalid credentials...")
    
    # Test invalid credentials
    credentials = f"invalid_user:invalid_pass"
    encoded = base64.b64encode(credentials.encode()).decode()
    invalid_headers = {"Authorization": f"Basic {encoded}"}
    
    response = client.get(f"{BASE_URL}/api/links/", headers=invalid_headers)
    assert response.status_code == 401
    print("Invalid credentials rejected")
