import boto3
import logging
import json

import helpers.utils as utils

from configuration import REGION_OREGON, socioBasket, GAH_PAGE_ID, LIVE_PERSON_INTENT_IDS
from resources.aws_lambda import (
    QUEUE_PERCENT_LAMBDA
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
invoke_lamdba = boto3.client("lambda", region_name = REGION_OREGON)



def get_work_basket(last_brand,payload):

    request_payload = {
        "last_brand" : last_brand,
        "payload" : payload
    }

    try:
        logger.info(f"Request [{QUEUE_PERCENT_LAMBDA}]: {request_payload}")
        get_distribution_wb = invoke_lamdba.invoke(FunctionName = QUEUE_PERCENT_LAMBDA, InvocationType = "RequestResponse", Payload = json.dumps(request_payload))
        get_distribution_wb = json.loads(get_distribution_wb['Payload'].read().decode())
        logger.info(f"Response [{QUEUE_PERCENT_LAMBDA}]: {get_distribution_wb}")
        return get_distribution_wb
    except Exception as error:
        logger.error(f"Failed to invoke: {QUEUE_PERCENT_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}

def percentage_routing_checker(intent_id, page_id):
    if intent_id == LIVE_PERSON_INTENT_IDS['prepaid-regular']:
        return 'prepaid'
    if intent_id == LIVE_PERSON_INTENT_IDS['postpaid-regular']:
        return 'postpaid'
    if intent_id == LIVE_PERSON_INTENT_IDS['broadband-regular']:
        return 'broadband'
    if intent_id == LIVE_PERSON_INTENT_IDS['hpw-regular']:
        return 'hpw'    
    if intent_id == socioBasket[page_id]['broadband']:
        return "broadband"
    # if page_id == GAH_PAGE_ID and intent_id in [socioBasket[page_id]['broadband'], socioBasket[page_id]['main']]:
    #     return "broadband"
    # if intent_id == socioBasket[page_id]['hpw']:
    #     return "hpw"
    # if intent_id == socioBasket[page_id]['postpaid']:
    #     return "postpaid"
    # if intent_id == socioBasket[page_id]['prepaid']:
    #     return "prepaid"
    return None
    
    