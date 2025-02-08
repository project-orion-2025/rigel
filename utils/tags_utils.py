"""Utility functions for Tags API testing."""

import requests
import logging
from typing import Dict, Any, Optional, List
from configs.tags_config import HEADERS, EXPECTED_TAG_FIELDS, generate_auth_token

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_request(
    method: str,
    url: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None
) -> requests.Response:
    """
    Make an HTTP request to the Tags API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        url: API endpoint URL
        data: Request payload (optional)
        params: Query parameters (optional)
    
    Returns:
        requests.Response object
    
    Raises:
        requests.exceptions.HTTPError: If the API returns an error response
    """
    try:
        # Get headers
        headers = HEADERS.copy()
        
        # Add auth token only for non-public endpoints
        if "/public/" not in url:
            token = generate_auth_token()
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.request(
            method=method.upper(),
            url=url,
            json=data if data else None,
            params=params,
            headers=headers
        )
        logger.info(f"{method} request to {url} - Status: {response.status_code}")
        
        # Raise HTTPError for error responses
        if response.status_code >= 400:
            logger.error(f"API error: {response.text}")
            response.raise_for_status()
        
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise

def validate_tag_response(response_data: Dict[str, Any]) -> bool:
    """
    Validate that a tag response contains all required fields.
    
    Args:
        response_data: JSON response from the API
    
    Returns:
        bool: True if all required fields are present, False otherwise
    """
    return all(field in response_data for field in EXPECTED_TAG_FIELDS)

def validate_tags_list_response(response_data: List[Dict[str, Any]]) -> bool:
    """
    Validate that a list of tags contains valid tag objects.
    
    Args:
        response_data: List of tag objects from the API
    
    Returns:
        bool: True if all tags are valid, False otherwise
    """
    return all(validate_tag_response(tag) for tag in response_data)
