import requests as rq
import random
import configs.config as config

# import faker

def generate_payload():
    # random_text = faker.Faker().sentence()
    random_int = random.random()
    payload ={
        "title": f"This is a text{random_int}", # {random_text}
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

generated_payload = generate_payload()
    
def create_question_id():
    payload = generate_payload()  # Generate a fresh payload for each call
    create_question_response = rq.post(config.CREATE_QUESTION_URL, json=payload)
    assert create_question_response.status_code == 201
    question_data = create_question_response.json()
    question_id = question_data["questionId"]
    return question_id