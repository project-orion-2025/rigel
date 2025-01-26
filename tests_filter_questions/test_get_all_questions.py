# Tests/test_get_all_questions.py
import pytest
import requests as rq
import configs.config as config


@pytest.mark.pagination
def test_get_all_questions_valid():
    """
    Test fetching all questions with valid parameters.
    """
    response = rq.get(config.GET_ALL_QUESTION_URL, params={"pageNumber": 0, "pageSize": 2})
    assert response.status_code == 200, "Expected status code 200 for valid request"
    response_json = response.json()
    assert "content" in response_json, "Response should contain 'content'"
    assert isinstance(response_json["content"], list), "'content' should be a list"


@pytest.mark.pagination
def test_get_all_questions_missing_params():
    """
    Test fetching all questions with missing parameters (should use defaults).
    """
    response = rq.get(config.GET_ALL_QUESTION_URL)
    assert response.status_code == 200, "Expected status code 200 for valid request"


@pytest.mark.pagination
def test_get_all_questions_invalid_page_number():
    """
    Test fetching all questions with an invalid page number.
    """
    response = rq.get(config.GET_ALL_QUESTION_URL, params={"pageNumber": -1, "pageSize": 2})
    assert response.status_code in [200, 400], "Unexpected status code for invalid page number"


@pytest.mark.pagination
def test_get_all_questions_large_page_size():
    """
    Test fetching all questions with a large page size.
    """
    response = rq.get(config.GET_ALL_QUESTION_URL, params={"pageNumber": 0, "pageSize": 1000})
    assert response.status_code == 200, "Expected status code 200 for large page size"


@pytest.mark.sorting
def test_get_all_questions_sort_by_question_id_desc():
    """
    Test fetching all questions sorted by questionId in descending order.
    """
    response = rq.get(
        config.GET_ALL_QUESTION_URL,
        params={"pageNumber": 0, "pageSize": 5, "sortBy": "questionId", "sortOrder": "desc"}
    )
    assert response.status_code == 200, "Expected status code 200 for valid request"
    response_json = response.json()
    assert "content" in response_json, "Response should contain 'content'"
    assert isinstance(response_json["content"], list), "'content' should be a list"
    if len(response_json["content"]) > 1:
        question_ids = [question["questionId"] for question in response_json["content"]]
        assert question_ids == sorted(question_ids, reverse=True), "Questions should be sorted in descending order"
