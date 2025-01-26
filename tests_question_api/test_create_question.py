import requests as rq
import random
import configs.config as config
import utils.question_utils as question_utils
import faker


# Data is fetched from the endpoint.
endpoint =  config.ENDPOINT

# Function to create a test
def test_create_question():
    payload = question_utils.generate_payload()  # Generate a fresh payload for each call
    
    # Testing whether payload is meeting the required conditions.
    assert 3 <= len(payload["title"]) <= 50, "Title must contain at least 3 characters and at most 50 characters."
    assert 6 <= len(payload["description"]) <= 1000, "Description must contain atleast 6 characters and atmost 1000 characters."
    assert payload["status"] in ["ACTIVE", "INACTIVE"], "Status must not be null, it should be active or inactive"
    assert payload["subject"] in ["CHEMISTRY", "PHYSICS", "MATH", "BIOLOGY"], "Subject must be one of the allowed values"
    assert payload["difficulty"] in ["EASY", "MEDIUM", "HARD"], "Difficulty must be one of the allowed values."
    assert len(payload["options"]) == 4, "Exactly 4 options are required."
    assert all("text" in option for option in payload["options"]), "Each option must have a text field"
    assert 1 <= payload["correctOptionId"] <= 4, "CorrectOptionId must be between 1 and 4"
    assert len(payload["tagList"]) >= 1, "At least one tag is required."
    
    # Create Question (After payload meets the requirements)
    
    create_question_response = rq.post(config.CREATE_QUESTION_URL, json=payload)
    assert create_question_response.status_code == 201
    question_data = create_question_response.json()
    question_id = question_data["questionId"]
    
    # Testing by getting the craeted question and matching it with the title
    get_question_response = rq.get(config.GET_QUESTION_URL + f"/{question_id}")
    assert get_question_response.status_code == 200
    get_question_data = get_question_response.json()
    
    # Testing for question and payload data match (Any three random key-value pairs)
    
    assert get_question_data["title"] == payload["title"], "title mismatch in fetched question."
    assert get_question_data["subject"] == payload["subject"], "subject mismatch in fetched question."