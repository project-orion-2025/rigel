"""Test cases for tag retrieval functionality."""

import pytest
import requests
from .base_test import BaseTestExecutor

class TestGetTag(BaseTestExecutor):
    """Test executor for tag retrieval operations."""

    def test_get_all_tags(self):
        """Test retrieving all tags."""
        response = self.make_request(
            method="GET",
            url=self.endpoints["get_all"]
        )
        
        assert response.status_code == 200
        tags = response.json()
        assert isinstance(tags, list)
        if tags:  # If any tags exist
            for tag in tags:
                assert isinstance(tag, dict)
                assert "text" in tag
                assert isinstance(tag["text"], str)

    def test_get_specific_tag(self):
        """Test retrieving a specific tag."""
        # First create a tag
        tag_name = "test-get-tag"
        tag_data = self.create_test_tag(tag_name)
        
        # Then retrieve it
        get_url = self.endpoints["get_one"].format(tag_name=tag_name)
        response = self.make_request(
            method="GET",
            url=get_url
        )
        
        if response.status_code == 200:
            tag = response.json()
            assert isinstance(tag, dict)
            assert "text" in tag
            assert isinstance(tag["text"], str)
        elif response.status_code == 401:
            error_response = response.json()
            assert error_response == {
                "error": "Unauthorized",
                "message": "Full authentication is required to access this resource",
                "path": "/error",
                "status": 401
            }
        else:
            assert False, f"Unexpected status code: {response.status_code}"

    def test_get_nonexistent_tag(self):
        """Test retrieving a non-existent tag."""
        nonexistent_tag = "nonexistent-tag"
        url = self.endpoints["get_one"].format(tag_name=nonexistent_tag)
        
        response = self.make_request(
            method="GET",
            url=url
        )
        assert response.status_code == 401  # API returns 401 for unauthorized access
        error_response = response.json()
        assert error_response == {
            "error": "Unauthorized",
            "message": "Full authentication is required to access this resource",
            "path": "/error",
            "status": 401
        }
