"""
Configuration settings for Tags API testing.

@author: siva shankar
@doc: All the endpoints and authentication configuration will be fetched from here
"""

import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Update these values if your API is running elsewhere
BASE_URL = "http://localhost:8080"  # Change if needed

# Authentication credentials
AUTH_CREDENTIALS = {
    "username": "Sai11",  # Verify these credentials
    "password": "SaiPassCode123"
}

# Initialize auth token
AUTH_TOKEN = None

def generate_auth_token():
    """Generate JWT token using username/password authentication."""
    global AUTH_TOKEN
    try:
        logger.info("Generating new auth token...")
        signin_response = requests.post(
            f"{BASE_URL}/api/auth/public/signin",  
            json=AUTH_CREDENTIALS,
            headers={"Content-Type": "application/json"}
        )
        
        if signin_response.status_code == 200:
            data = signin_response.json()
            AUTH_TOKEN = data.get("jwtToken")
            if AUTH_TOKEN:
                logger.info("Successfully generated auth token")
                return AUTH_TOKEN
        
        logger.error(f"Auth failed with status {signin_response.status_code}")
        logger.error(f"Response: {signin_response.text}")
        raise ValueError("Failed to get valid auth token")
            
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise

# API Endpoints
TAGS_ENDPOINTS = {
    "create": f"{BASE_URL}/api/author/tags",  # tagName will be added as query param
    "get_all": f"{BASE_URL}/api/public/tags",
    "get_one": f"{BASE_URL}/api/public/tags/{{tag_name}}",
    "update": f"{BASE_URL}/api/author/tags",  # tagName will be added as query param
    "delete": f"{BASE_URL}/api/author/tags/{{tag_id}}"
}

# Headers for API requests
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def get_auth_headers():
    """Get headers with current auth token"""
    headers = HEADERS.copy()
    token = generate_auth_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

# Test Data
TEST_TAG_DATA = {
    "name": "test-tag",
    "description": "A test tag for API testing"
}

# Expected response fields
EXPECTED_TAG_FIELDS = ["tagId", "text"]
