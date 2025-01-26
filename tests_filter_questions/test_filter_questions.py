import pytest
import requests as rq
import configs.config as config
import utils.filter_question_utils as question_utils


@pytest.fixture
def search_payload():
    """
    Provides a mock payload for the search API.

    Returns:
        dict: Mock search payload.
    """
    return question_utils.get_mock_search_payload()


@pytest.fixture
def expected_question_structure():
    """
    Defines the expected structure of a question in the response.

    Returns:
        dict: Expected question structure with field types.
    """
    return {
        "questionId": int,
        "title": str,
        "description": str,
        "author": str,
        "status": str,
        "subject": str,
        "difficulty": str,
        "options": list,
        "tagList": list,
        "correctOptionId": (int, type(None))
    }


@pytest.fixture
def expected_pagination_structure():
    """
    Defines the expected structure of pagination data in the response.

    Returns:
        dict: Expected pagination structure with field types.
    """
    return {
        "pageNumber": int,
        "pageSize": int,
        "totalElements": int,
        "totalPages": int,
        "lastPage": bool
    }


def test_search_questions_valid(search_payload):
    """
    Test searching questions with a valid payload.
    """
    response = rq.post(config.SEARCH_QUESTION_URL, json=search_payload)
    assert response.status_code == 200, "Expected status code 200 for a valid request"
    response_json = response.json()
    assert "content" in response_json, "Response should contain 'content'"
    assert isinstance(response_json["content"], list), "'content' should be a list"


def test_search_questions_invalid_payload():
    """
    Test searching questions with an invalid payload.
    """
    invalid_payload = {"invalid_field": "invalid_value"}
    response = rq.post(config.SEARCH_QUESTION_URL, json=invalid_payload)
    assert response.status_code == 400, "Expected status code 400 for invalid payload"


def test_question_structure(search_payload, expected_question_structure):
    """
    Test that each question matches the expected structure.
    """
    response = rq.post(config.SEARCH_QUESTION_URL, json=search_payload)
    assert response.status_code == 200
    
    data = response.json()
    for question in data["content"]:
        for field, expected_type in expected_question_structure.items():
            assert field in question, f"Missing required field: {field}"
            if isinstance(expected_type, tuple):
                assert isinstance(question[field], expected_type), \
                    f"Incorrect type for {field}. Expected one of {expected_type}, got {type(question[field])}"
            else:
                assert isinstance(question[field], expected_type), \
                    f"Incorrect type for {field}. Expected {expected_type}, got {type(question[field])}"


def test_pagination_structure(search_payload, expected_pagination_structure):
    """
    Test that pagination data matches the expected structure.
    """
    response = rq.post(config.SEARCH_QUESTION_URL, json=search_payload)
    assert response.status_code == 200

    data = response.json()
    for field, expected_type in expected_pagination_structure.items():
        assert field in data, f"Missing pagination field: {field}"
        assert isinstance(data[field], expected_type), \
            f"Incorrect type for pagination field {field}. Expected {expected_type}, got {type(data[field])}"
