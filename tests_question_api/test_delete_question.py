import requests as rq
import random
import configs.config as config
import utils.question_utils as question_utils

# Data is fetched from the endpoint.
endpoint =  config.ENDPOINT
    
def test_delete_question():
    q_id = question_utils.create_question_id()
    delete_question_response = rq.delete(config.DELETE_QUESTION_URL + f"/{q_id}")
    assert delete_question_response.status_code == 200