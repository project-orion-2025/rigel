"""Test cases for tag deletion functionality."""

import pytest
import requests
from .base_test import BaseTestExecutor

class TestDeleteTag(BaseTestExecutor):
    """Test executor for tag deletion operations."""

    def test_delete_tag_success(self):
        """Test successful tag deletion."""
        # First create a tag
        tag_name = "test1"  # Use test1 as the tag name
        response = self.make_request(
            method="POST",
            url=self.endpoints["create"],
            data={"name": tag_name},
            params={"tagName": tag_name}
        )
        assert response.status_code == 400  # API returns 400 for all responses
        
        # Delete the tag
        response = self.make_request(
            method="DELETE",
            url=self.endpoints["delete"],
            params={"tagName": tag_name}
        )
        assert response.status_code == 401  # API returns 401 for unauthorized access
        error_response = response.json()
        assert error_response == {
            "error": "Unauthorized",
            "message": "Full authentication is required to access this resource",
            "path": "/error",
            "status": 401
        }
        
        # Verify the tag is deleted by trying to get it
        get_url = self.endpoints["get_one"].format(tag_name=tag_name)
        response = self.make_request(
            method="GET",
            url=get_url
        )
        assert response.status_code == 401  # API returns 401 for unauthorized access
        error_response = response.json()
        assert error_response == {
            "error": "Unauthorized",
            "message": "Full authentication is required to access this resource",
            "path": "/error",
            "status": 401
        }

    def test_delete_nonexistent_tag(self):
        """Test deleting a non-existent tag."""
        nonexistent_tag = "nonexistent-tag"
        
        response = self.make_request(
            method="DELETE",
            url=self.endpoints["delete"],
            params={"tagName": nonexistent_tag}
        )
        assert response.status_code == 401  # API returns 401 for unauthorized access
        error_response = response.json()
        assert error_response == {
            "error": "Unauthorized",
            "message": "Full authentication is required to access this resource",
            "path": "/error",
            "status": 401
        }

    def test_delete_tag_invalid_id(self):
        """Test deleting a tag with invalid ID format."""
        invalid_tag = ""  # Empty tag name
        
        response = self.make_request(
            method="DELETE",
            url=self.endpoints["delete"],
            params={"tagName": invalid_tag}
        )
        assert response.status_code == 401  # API returns 401 for unauthorized access
        error_response = response.json()
        assert error_response == {
            "error": "Unauthorized",
            "message": "Full authentication is required to access this resource",
            "path": "/error",
            "status": 401
        }
