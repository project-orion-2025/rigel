"""Base test executor class for API testing."""

import pytest
import requests
from typing import Dict, Any, Optional, List

from configs.tags_config import TAGS_ENDPOINTS, get_auth_headers
from utils.tags_utils import make_request, validate_tag_response, validate_tags_list_response

class BaseTestExecutor:
    """Base class for all API test executors."""
    
    @pytest.fixture(autouse=True)
    def setup_test(self) -> None:
        """Set up test environment before each test."""
        self.endpoints = TAGS_ENDPOINTS
        self.headers = get_auth_headers()
        yield
    
    def make_request(
        self,
        method: str,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """Make an API request with proper error handling."""
        return make_request(method, url, data, params)
    
    def create_test_tag(self, tag_name: str) -> Dict[str, Any]:
        """Helper method to create a test tag."""
        url = self.endpoints["create"]
        response = self.make_request(
            "POST", 
            url, 
            data={"name": tag_name}, 
            params={"tagName": tag_name}
        )
        return response.json()
    
    def delete_test_tag(self, tag_id: str) -> None:
        """Helper method to delete a test tag."""
        url = self.endpoints["delete"].format(tag_id=tag_id)
        self.make_request("DELETE", url)
    
    def verify_tag_response(self, response_data: Dict[str, Any]) -> bool:
        """Verify tag response format."""
        return validate_tag_response(response_data)
    
    def verify_tags_list_response(self, response_data: List[Dict[str, Any]]) -> bool:
        """Verify list of tags response format."""
        return validate_tags_list_response(response_data)
