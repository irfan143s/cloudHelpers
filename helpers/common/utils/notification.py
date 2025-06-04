import copy
import logging

import resources.common.constants.templates as templates
import helpers.common.utils.api as common_api_utils

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def send_sms(**kwargs):
    payload = copy.deepcopy(templates.CONNECT_LMB_REQUEST)

    sms_receiver = kwargs.get("receiver", "")
    message_id = kwargs.get("message_id", "")
    parameters = kwargs.get("parameters", {})
    
    logger.info(f"send_sms kwargs: {kwargs}")
    
    if not sms_receiver:
        logger.info(f"sms_receiver attribute is required")
        return False
    if not message_id:
        logger.info(f"message_id attribute is required")
        return False
    
    payload["Details"]["Parameters"]["smsReceiver"] = sms_receiver
    payload["Details"]["Parameters"]["messageId"] = message_id
    payload["Details"]["Parameters"].update(parameters)

    common_api_utils.publish_sms_through_raven(payload = payload)

