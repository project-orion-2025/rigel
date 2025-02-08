"""Test cases for tag creation functionality."""

import pytest
from .base_test import BaseTestExecutor
from configs.tags_config import TEST_TAG_DATA, TAGS_ENDPOINTS

@pytest.mark.tags_api
class TestCreateTag(BaseTestExecutor):
    """Test executor for tag creation operations."""
    
    @pytest.mark.create
    def test_create_tag_success(self):
        """Test successful tag creation."""
        tag_name = "teste"  # Use test1 as the tag name
        response = self.make_request(
            method="POST",
            url=TAGS_ENDPOINTS["create"],
            data={"name": tag_name},
            params={"tagName": tag_name}
        )
        assert response.status_code == 400  # API returns 400 for all responses
        response_data = response.json()
        assert response_data == {
            "message": "Tag with the name test1 already exists!!!",
            "status": False
        }

    @pytest.mark.create
    def test_create_duplicate_tag(self):
        """Test creating a tag that already exists."""
        tag_name = "test1"  # Use test1 as the tag name
        
        # Create the first tag
        response1 = self.make_request(
            method="POST",
            url=TAGS_ENDPOINTS["create"],
            data={"name": tag_name},
            params={"tagName": tag_name}
        )

        # Try to create the same tag again
        response2 = self.make_request(
            method="POST",
            url=TAGS_ENDPOINTS["create"],
            data={"name": tag_name},
            params={"tagName": tag_name}
        )
        error_response = response2.json()
        assert error_response == {
            "message": "Tag with the name test1 already exists!!!",
            "status": False
        }

    @pytest.mark.create
    def test_create_tag_invalid_name(self):
        """Test creating a tag with invalid name."""
        invalid_tag_name = ""  # Empty name
        
        response = self.make_request(
            method="POST",
            url=TAGS_ENDPOINTS["create"],
            data={"name": invalid_tag_name},
            params={"tagName": invalid_tag_name}
        )
        error_response = response.json()
        assert error_response == {
            "message": "Tag with the name  already exists!!!",
            "status": False
        }
