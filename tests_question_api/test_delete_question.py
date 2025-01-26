import requests as rq
import random
import configs.config as config
import utils.question_utils as question_utils

# Data is fetched from the endpoint.
endpoint =  config.ENDPOINT
    
def test_delete_question():
    q_id = question_utils.create_question_id()
    delete_question_response = rq.delete(config.DELETE_QUESTION_URL + f"/{q_id}")
    assert delete_question_response.status_code == 200, "Can't perform operation.(question may not found or already deleted)"
    question_data = delete_question_response.json()
    assert question_data["questionId"] == q_id, "Deleted question ID does not match."
    
    get_question_response = rq.get(config.GET_QUESTION_URL + f"/{q_id}")
    assert get_question_response.status_code == 404, "Question found."
    error_message = get_question_response.json()
    assert error_message["message"] == f"Question not found with questionId: {q_id}", "Unexpected error message for deleted question."
    