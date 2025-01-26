import requests as rq
import random
import configs.config as config
import utils.question_utils as question_utils

# Data is fetched from the endpoint.
endpoint =  config.ENDPOINT

# For updating we need to first create question
# Then update question
# Then get question and verify
def test_update_question():
    q_id = question_utils.create_question_id()
    payload_for_update = question_utils.generate_payload()
    update_question_response = rq.put(config.UPDATE_QUESTION_URL + f"/{q_id}", json = payload_for_update)
    assert update_question_response.status_code == 200, "Failed to update question"
    get_question_response = rq.get(config.GET_QUESTION_URL + f"/{q_id}")
    updated_data = get_question_response.json()
    assert updated_data["title"] == payload_for_update["title"], "Title was not updated correctly."
    assert updated_data["description"] == payload_for_update["description"], "Description was not updated correctly."
    assert updated_data["status"] == payload_for_update["status"], "Status was not updated correctly."
    
