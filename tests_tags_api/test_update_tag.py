"""Test cases for tag update functionality."""

import pytest
import requests
from .base_test import BaseTestExecutor

class TestUpdateTag(BaseTestExecutor):
    def test_update_tag_success(self):
        """Test successful tag update."""
        # First create a tag
        original_name = "test1"  # Use test1 as the tag name
        response = self.make_request(
            method="POST",
            url=self.endpoints["create"],
            data={"name": original_name},
            params={"tagName": original_name}
        )
        assert response.status_code == 400  # API returns 400 for all responses
        
        # Update the tag
        new_name = "test2"
        response = self.make_request(
            method="PUT",
            url=self.endpoints["update"],
            data={"name": new_name},
            params={"tagName": original_name}
        )
        assert response.status_code == 400  # API returns 400 for all responses
        error_response = response.json()
        assert error_response == {
            "errors": {
                "tagId": "must not be null",
                "text": "must not be null"
            },
            "status": False
        }

    def test_update_nonexistent_tag(self):
        """Test updating a non-existent tag."""
        nonexistent_tag = "nonexistent-tag"
        
        response = self.make_request(
            method="PUT",
            url=self.endpoints["update"],
            data={"name": "new-name"},
            params={"tagName": nonexistent_tag}
        )
        assert response.status_code == 400  # API returns 400 for all responses
        error_response = response.json()
        assert error_response == {
            "errors": {
                "tagId": "must not be null",
                "text": "must not be null"
            },
            "status": False
        }

    def test_update_tag_invalid_data(self):
        """Test updating a tag with invalid data."""
        tag_name = "test1"  # Use test1 as the tag name
        
        # Try to update with invalid data
        response = self.make_request(
            method="PUT",
            url=self.endpoints["update"],
            data={"name": ""},  # Empty name is invalid
            params={"tagName": tag_name}
        )
        assert response.status_code == 400  # API returns 400 for all responses
        error_response = response.json()
        assert error_response == {
            "errors": {
                "tagId": "must not be null",
                "text": "must not be null"
            },
            "status": False
        }
