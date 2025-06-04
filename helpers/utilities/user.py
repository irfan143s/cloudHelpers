# NIAS 2.0 - HISAMS
import logging

from helpers.utils import (
    get_10_digit_mobile_number
)
import helpers.whitelistchecker as whitelistchecker

from helpers.ddbtools import DDBTools

import resources.resourcemapping  as resourcemapping
import resources.constants as constants
import resources.tableattributes as tableattributes

import configuration as configs

logger = logging.getLogger()
logger.setLevel(logging.INFO)


"""****************************************************************************************
***** Put Facebook user context methods here if being used on multiple places *************
****************************************************************************************"""

def is_vip_user(**kwargs) -> bool:
    concern_no = kwargs.get("concern_no", "")

    if not concern_no:
        return False

    if whitelistchecker.is_employee_care_whitelisted(get_10_digit_mobile_number(concern_no)) or whitelistchecker.is_employee_care_whitelisted(concern_no):
        return True
    return False


def is_active_bot_session(request: dict, ddb_session) -> bool:
    
    logger.info(f"Checking if user is having a bot session")
    response = ddb_session.get_item('fbId',request['fbId'])
    logger.info(f"Session table response: {response}")

    if len(response) and response[0]["status"] != constants.SESSION_STATUS_TICKET_CLOSURE:
        logger.info(f'User is having a bot session: {resourcemapping.page_name_mapping_dict[response[0]["pageId"]]}')
        return True

    logger.info(f"User is not having a bot session")
    return False


""" This checks if the webhook event is initiated by the user. """
def is_valid_user_event(request: dict) -> bool:
    logger.info(f"is_valid_user_event: {request}")

    VALID_USER_EVENT_MESSAGING_KEYS = ["postback", "message", "referral"]
    VALID_USER_EVENT_MESSAGING_MESSAGE_KEYS = ["attachments", "quick_reply", "text"]

    event_entry = request['body-json']['entry'][0]

    if "messaging" not in event_entry.keys():
        return False

    event_messaging = event_entry['messaging'][0]
    
    if not any(key in event_messaging.keys() for key in VALID_USER_EVENT_MESSAGING_KEYS):
        return False

    if "message" in event_messaging.keys():
        if not any(key in event_messaging["message"].keys() for key in VALID_USER_EVENT_MESSAGING_MESSAGE_KEYS):
            return False

    if "pass_thread_control" in event_messaging.keys():
        return False
    
    return True


def is_user_thea_registered(pageid:str, psid:str, identitykey: str = "") -> bool:
    logger.info(f"is_user_thea_registered: pageid={pageid}, psid={psid}, identitykey={identitykey}")
    thea_psid = psid

    if pageid != configs.THEA_PAGE_ID:
        logger.info(f"Current page is not thea.")
        ddb_identity = DDBTools(configs.DDB_FACEBOOK_USER_IDENTITY, configs.REGION_OREGON)
        thea_identity_attr_name, thea_identity_idx_name = get_user_identity_attributes(configs.THEA_PAGE_ID)
        identity_data = {}

        if identitykey:
            ddb_identity_res = ddb_identity.get_item(tableattributes.IDENTITY_KEY, identitykey)
            if len(ddb_identity_res):
                identity_data = ddb_identity_res[0]

        if not identity_data:
            curr_page_attr_name, curr_page_idx_name = get_user_identity_attributes(pageid)
            ddb_identity_by_idx_res = ddb_identity.get_item_by_index(curr_page_attr_name, psid, curr_page_idx_name)
            
            if len(ddb_identity_by_idx_res):
                identity_data = ddb_identity_by_idx_res[0]
            else:
                logger.info(f"Identity data cannot be found.")
                return False

        if thea_identity_attr_name in identity_data.keys():
            thea_psid = identity_data[thea_identity_attr_name]
        else:
            logger.info(f"Identity data does not contains {thea_identity_attr_name}")
            return False

        logger.info(f"Identity data found: {identity_data}")


    ddb_thea_main = DDBTools(resourcemapping.page_ddb_mapping_dict[configs.THEA_PAGE_ID]["main"], configs.REGION_OREGON)
    thea_main_res = ddb_thea_main.get_item(tableattributes.FB_ID, thea_psid)
    thea_main_data = {}

    if len(thea_main_res):
        thea_main_data = thea_main_res[0]
    else:
        logger.info(f"User has no record on thea main.")
        return False

    registered_date = thea_main_data.get(tableattributes.REGISTERED_DATE, "")
    registered_number = thea_main_data.get(tableattributes.REGISTERED_NUMBER, "")

    logger.info(f"registered_date={registered_date}, registered_number={registered_number}")

    if not registered_date or registered_date in ["string", "none"]:
        logger.info(f"No registeredDate found or is invalid.")
        return False

    if not registered_number or registered_number.strip().lower() in ["string", "none"]:
        logger.info(f"No registered number found or is invalid.")
        return False

    if not whitelistchecker.is_platinum_whitelisted(registered_number):
        logger.info(f"registered number {registered_number} is not Platinum whtelisted.")
        return False

    logger.info(f"User is thea registered.")
    return True


def get_user_identity_attributes(pageid:str) -> tuple:
    attr_name = resourcemapping.SINGLE_IDENTITY_KEY_ATTRIBUTES[pageid]["attribute_name"]
    idx_name = resourcemapping.SINGLE_IDENTITY_KEY_ATTRIBUTES[pageid]["index_name"]
    return (attr_name, idx_name)

def is_customer_verification_done(**kwargs) -> bool:
    request = kwargs.get("request", {})
    logger.info(f"isVerification req: {request}")
    sessionAttr = request.get("sessionContextAttributes", {})

    if configs.SWITCH_CUSTOMER_VERIFICATION == 'ON':
        if sessionAttr:
            return sessionAttr.get("isVerificationDone", False) 
        else:
            return False
    else:
        return True