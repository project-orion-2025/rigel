import requests as rq
import random
import configs.config as config


def fetch_all_questions(params=None):
    """
    Fetch all questions from the API with optional query parameters.

    Args:
        params (dict, optional): Query parameters for filtering questions.

    Returns:
        dict: JSON response containing question data.

    Raises:
        Exception: If the response status code is not 200.
    """
    response = rq.get(config.GET_ALL_QUESTION_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch questions. Status code: {response.status_code}")
    return response.json()


def search_questions(payload=None):
    """
    Search for questions based on filters.

    Args:
        payload (dict, optional): JSON payload for filtering questions.

    Returns:
        dict: JSON response containing filtered questions.

    Raises:
        Exception: If the response status code is not 200.
    """
    response = rq.post(config.SEARCH_QUESTION_URL, json=payload)
    if response.status_code != 200:
        raise Exception(f"Search API failed. Status code: {response.status_code}")
    return response.json()


def generate_payload():
    """
    Generate a payload for creating a new question.

    Returns:
        dict: A dictionary containing question data.
    """
    random_int = random.randint(1000, 9999)  # Ensure consistent uniqueness
    payload = {
        "title": f"This is a question {random_int}",
        "description": "Choose the correct answer.",
        "subject": "CHEMISTRY",
        "difficulty": "MEDIUM",
        "status": "ACTIVE",
        "author": "Kushidhar",
        "options": [
            {"text": "Option A"},
            {"text": "Option B"},
            {"text": "Option C"},
            {"text": "Option D"}
        ],
        "tagList": [
            {"text": "example"},
            {"text": "test"}
        ],
        "correctOptionId": 1
    }
    return payload


def create_question_id():
    """
    Create a new question and return its ID.

    Returns:
        int: The ID of the created question.

    Raises:
        Exception: If the response status code is not 201.
    """
    payload = generate_payload()
    response = rq.post(config.CREATE_QUESTION_URL, json=payload)
    if response.status_code != 201:
        raise Exception(f"Failed to create question. Status code: {response.status_code}")
    return response.json().get("questionId")


def get_mock_search_payload():
    """
    Returns a mock payload for the search API.

    Returns:
        dict: A dictionary representing mock search filters.
    """
    return {
        "subject": "CHEMISTRY",
        "difficulty": "MEDIUM",
        "title": "Sample Title",
        "tagList": [1, 2]
    }


def get_mock_all_questions_response():
    """
    Returns a mock response for the 'Get All Questions' API.

    Returns:
        dict: A dictionary representing a mock response with questions.
    """
    return {
        "content": [
            {
                "questionId": 1,
                "title": "What is the atomic number of Hydrogen?",
                "description": "Choose the correct answer.",
                "author": "Kushidhar",
                "status": "ACTIVE",
                "subject": "CHEMISTRY",
                "difficulty": "EASY",
                "options": [
                    {"optionId": 1, "text": "1"},
                    {"optionId": 2, "text": "2"},
                    {"optionId": 3, "text": "3"},
                    {"optionId": 4, "text": "4"}
                ],
                "tagList": [
                    {"tagId": 1, "text": "periodic_table"},
                    {"tagId": 2, "text": "hydrogen"}
                ],
                "correctOptionId": 1
            }
        ],
        "pageNumber": 0,
        "pageSize": 10,
        "totalElements": 1,
        "totalPages": 1,
        "lastPage": True
    }
