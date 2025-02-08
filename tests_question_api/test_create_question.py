import requests as rq
import configs.config as config
import utils.question_utils as question_utils

# Function to create a test
def test_create_question():
    token = config.AUTH_TOKEN  # Ensure the token is stored in the config file
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    payload = question_utils.generate_payload()  # Generate a fresh payload for each call

    # Testing whether payload meets required conditions
    assert 3 <= len(payload["title"]) <= 50, "Title must contain at least 3 characters and at most 50 characters."
    assert 6 <= len(payload["description"]) <= 1000, "Description must contain at least 6 characters and at most 1000 characters."
    assert payload["status"] in ["ACTIVE", "INACTIVE"], "Status must be either ACTIVE or INACTIVE."
    assert payload["subject"] in ["CHEMISTRY", "PHYSICS", "MATH", "BIOLOGY"], "Invalid subject."
    assert payload["difficulty"] in ["EASY", "MEDIUM", "HARD"], "Invalid difficulty level."
    assert len(payload["options"]) == 4, "Exactly 4 options are required."
    assert all("text" in option for option in payload["options"]), "Each option must have a text field."
    assert 1 <= payload["correctOptionId"] <= 4, "CorrectOptionId must be between 1 and 4."
    assert len(payload["tagList"]) >= 1, "At least one tag is required."

    # Create Question
    create_question_response = rq.post(config.CREATE_QUESTION_URL, json=payload, headers=headers)
    assert create_question_response.status_code == 201, f"Failed to create question: {create_question_response.text}"
    
    question_data = create_question_response.json()
    question_id = question_data["questionId"]

    # Retrieve and validate the created question
    get_question_response = rq.get(f"{config.GET_QUESTION_URL}/{question_id}", headers=headers)
    assert get_question_response.status_code == 200, f"Failed to fetch question: {get_question_response.text}"
    
    get_question_data = get_question_response.json()

    # Validating retrieved data
    assert get_question_data["title"] == payload["title"], "Title mismatch."
    assert get_question_data["subject"] == payload["subject"], "Subject mismatch."
