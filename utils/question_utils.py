import requests as rq
import random
import configs.config as config

# import faker

def generate_payload():
    # random_text = faker.Faker().sentence()
    random_num = random.random()
    payload ={
        "title": f"This is a text{random_num}", # {random_text}
        "description": "Choose the correct answer.",
        "subject": "CHEMISTRY",
        "difficulty": "MEDIUM",
        "status": "ACTIVE",
        "author": "Kushidhar",
        "options": [
            {
                "text": "1"
            },
            {
                "text": "2"
            },
            {
                "text": "3"
            },
            {
                "text": "4"
            }
        ],
        "tagList": [
            {
                "text": "human"
            },
            {
                "text": "jio"
            }
        ],
        "correctOptionId": 1
    }
    return payload
    
def create_question_id():
    payload = generate_payload()  # Generate a fresh payload for each call
    
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
    
    create_question_response = rq.post(config.CREATE_QUESTION_URL, json=payload)
    assert create_question_response.status_code == 201, "Failed to create question."
    question_data = create_question_response.json()
    question_id = question_data["questionId"]
    return question_id