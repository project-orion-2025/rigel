"""
author :: siva shankar
@doc: all the end points will be fetched from here
"""

import requests as rq

ENDPOINT = "http://localhost:8080"

payload_for_signin = {
	"username": "siva54",
	"password": "Password"
}

AUTH_TOKEN = None  # Initialize as None

def gen_auth_token():
    global AUTH_TOKEN
    if AUTH_TOKEN is None:  # Generate only if not already generated
        signin_response = rq.post(f"{ENDPOINT}/api/auth/public/signin", json=payload_for_signin)
        assert signin_response.status_code == 200, "INVALID USER"
        data = signin_response.json()
        AUTH_TOKEN = data["jwtToken"]
    return AUTH_TOKEN

# Generate token once and store it
AUTH_TOKEN = gen_auth_token()

CREATE_QUESTION_URL = ENDPOINT + "/api/author/questions"

GET_QUESTION_URL = ENDPOINT + "/api/public/question"

UPDATE_QUESTION_URL = ENDPOINT + "/api/author/question"

DELETE_QUESTION_URL = ENDPOINT + "/api/author/question"

GET_ALL_QUESTION_URL = ENDPOINT + "/api/public/questions"

SEARCH_QUESTION_URL = ENDPOINT + "/api/public/question/search"
