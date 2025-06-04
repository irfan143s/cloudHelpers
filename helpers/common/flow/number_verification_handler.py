import logging
import re

from configuration import *
from resources.spiels import *
from resources.constants import *
from resources.common.constants.str import *
from resources.states import *
from helpers.common.utils.validation import is_valid_number
from helpers.customerjourneytools import CustomerJourney
from helpers.resFormatter import ResFormatter
from helpers.sessiontools import SessionTools
from helpers.unrecognizedloboptions import *

import helpers.common.utils.session as common_session_utils
import helpers.utilities.session as session_utils
import helpers.utilities.subscriber as subscriber_utils


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def number_verification_handler(**kwargs):
    init(**kwargs)

    return validate_number()


def init(**kwargs):
    global res, sender_id, page_id, message_type, event, message, lob_list, logger, session_tools, cj

    event = kwargs.get("Event", {})
    message_type = kwargs.get("MessageType", "")
    message = event.get("message", "")
    lob_list = kwargs.get("LobList", [])
    sender_id = event.get("fbId", "")
    page_id = event.get("channel", "")
    cj = kwargs.get("Cj", {})
    session_tools = SessionTools(sender_id, page_id)
    session_state = session_tools.get_session_state()


    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    res = ResFormatter(page_id)

def handle_get_number() -> None:
    if message_type == GET_NUMBER_NETWORK_CONCERN:
        res.send_message(sender_id, GET_NUMBER_NETWORK_CONCERN_SPIEL)
    elif message_type == GET_NUMBER_LOAD_PROMOS_AND_REWARDS:
        res.send_message(sender_id, GET_NUMBER_LOAD_PROMOS_AND_REWARDS_SPIEL)
    elif message_type == GET_NUMBER_BILLS_AND_PAYMENTS:
        res.send_message(sender_id, GET_NUMBER_BILLS_PAYMENT_SPIEL)
    elif message_type == GET_NUMBER_MODIFY_OR_TERMINATE:
        res.send_message(sender_id, GET_NUMBER_MODIFY_OR_TERMINATE_SPIEL)
    else:
        res.send_message(sender_id, GET_ALL_LOB_NUMBER_SPIEL)

def handle_number_not_existing() -> None:
    if message_type == GET_NUMBER_NETWORK_CONCERN:
        res.send_message(sender_id, NUMBER_INVALID_NETWORK_CONCERN_SPIEL)
    elif message_type == GET_NUMBER_LOAD_PROMOS_AND_REWARDS:
        res.send_message(sender_id, NUMBER_INVALID_LOAD_PROMOS_AND_REWARDS_SPIEL)
    elif message_type == GET_NUMBER_BILLS_AND_PAYMENTS:
        res.send_message(sender_id, NUMBER_INVALID_BILLS_AND_PAYMENTS_SPIEL)
    elif message_type == GET_NUMBER_MODIFY_OR_TERMINATE:
        res.send_message(sender_id, NUMBER_INVALID_MODIFY_AND_TERMINATE_SPIEL)
    else:
        res.send_message(sender_id, NUMBER_NOT_VALID_SPIEL)

def validate_number():              
    session_context_attributes = session_tools.get_session_context_attributes()
    check_number_confirmation = session_context_attributes.get("checkNumberConfirmation", "false")
    concern_number_confirmation = session_context_attributes.get("concernNumberConfirmation", "false")
    processed_number = session_context_attributes.get("processedNumber", message)
    processed_number = processed_number.replace(" ", "")
    if concern_number_confirmation == "true":
        
        session_tools.update_session_context_attributes({"concernNumberConfirmation": "false"})
        cleanMessage = re.sub("[^A-Za-z]", "", message.lower())
        messageToLower = message.lower()
        if cleanMessage == "yes" and (messageToLower.startswith("yes")):        
            common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1424", cj=cj)
            res.send_message(sender_id, GET_CONCERNED_NUMBER_ALL_LOB_SPIEL)
            res.send_message(sender_id, GET_ALL_LOB_NUMBER_SPIEL_GUIDELINES_2)
            common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1427", cj=cj)
        elif cleanMessage == "no" and (messageToLower.startswith("no")):
            session_tools.update_attributes({"unrecognizedRetry": "0"})
            common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1425", cj=cj)

            res.send_message(sender_id, NUMBER_NOT_EXISTING_CONFIRM_SPIEL)
            session_tools.update_sub_state('UNRECOGNIZED-INTENT-MENU-STATE')

            common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1428", cj=cj)
            render_spiels_options(session_attributes=event)
           
        else:
            common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1426", cj=cj)

            session_tools.update_sub_state('UNRECOGNIZED-INTENT-MENU-STATE')
            render_spiels_options(session_attributes=event) 

        return {
            "isValidated": True,
            "number": processed_number,
            "subscriberLob": "",
            "isExisting": False,
            "isValidLob": False
        }

    if check_number_confirmation == "false":
        common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1410", cj=cj)
        common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1411", cj=cj)
        validate_input_number()
    else: 
        clean_message = re.sub("[^A-Za-z]", "", message.lower())
        message_to_lower = message.lower()
        if clean_message == "yes" and (message_to_lower.startswith("yes")):
            common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1416", cj=cj)
            return validate_number_lob(processed_number)
        elif clean_message == "no" and (message_to_lower.startswith("no")):
            common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1417", cj=cj)
            if session_utils.is_global_retry_count_reached_threshold(session_tools = session_tools):
                common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1418", cj=cj)
                res.send_message(sender_id, INVALID_NUMBER_END_SPIEL_2)
                session_tools.reset_state_and_session()
            else:
                common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1419", cj=cj)              
                session_tools.update_session_context_attributes({"checkNumberConfirmation": "false"})
                session_utils.increase_global_retry_count(session_tools = session_tools)   
                handle_get_number()
                res.send_message(sender_id, GET_ALL_LOB_NUMBER_SPIEL_GUIDELINES_2)
        else:
            if session_utils.is_global_retry_count_reached_threshold(session_tools = session_tools):
                common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1420", cj=cj)
                session_tools.update_sub_state('UNRECOGNIZED-INTENT-MENU-STATE')
                common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1426", cj=cj)
                render_spiels_options(session_attributes=event)
                return {
                    "isValidated": False,
                    "number": processed_number,
                    "subscriberLob": "",
                    "isExisting": False,
                    "isValidLob": False
                }
            session_utils.increase_global_retry_count(session_tools = session_tools) 
            validate_input_number()
    return {
        "isValidated": False,
        "number": processed_number,
        "subscriberLob": "",
        "isExisting": False,
        "isValidLob": False
    }

def validate_input_number():
    message = event['message']
    mobile_number_object = is_valid_number(message)
    processed_number = mobile_number_object.get("validNumber", "")

    session_tools.update_session_context_attributes({"processedNumber": processed_number})

    session_context_attributes = session_tools.get_session_context_attributes()
    check_number_confirmation = session_context_attributes.get("checkNumberConfirmation", "false")

    if not mobile_number_object.get("isValid", False):
        logger.info(f"{processed_number}: invalid number")
        common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1413", cj=cj)

        if session_utils.is_global_retry_count_reached_threshold(session_tools = session_tools):
            if check_number_confirmation == "true":
                common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1420", cj=cj)
                session_tools.update_sub_state('UNRECOGNIZED-INTENT-MENU-STATE')
                common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1426", cj=cj)
                res.send_message(sender_id, UNRECOGNIZED_NUMBER_FORMAT_SPIEL_3)
                render_spiels_options(session_attributes=event)
                return
            else:
                common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1414", cj=cj)
                res.send_message(sender_id, INVALID_NUMBER_END_SPIEL_1)
                session_tools.reset_state_and_session()
                return
        if check_number_confirmation == "true": 
            common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1421", cj=cj)
            # session_utils.increase_global_retry_count(session_tools = session_tools)
            res.send_message(sender_id, UNRECOGNIZED_NUMBER_FORMAT_SPIEL_2)
            return
        else:
            common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1415", cj=cj)
            handle_invalid_input_number()
            return
    else: 
        common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1412", cj=cj)
        session_tools.update_session_context_attributes({"checkNumberConfirmation": "true"})
        res.send_quickresponse(
            sender_id, CONFIRM_FORMATED_NUMBER_SPIEL.format(mobile_number_object.get("validNumber", "")), YES_NO_MENU, MENU_FORM)


def handle_invalid_input_number():

    if session_utils.is_global_retry_count_reached_threshold(session_tools = session_tools):
        gibberish_log = {"flow": "validate concern no", "lob": "na", "message": event.get("message", ""), "psid": event.get("fbId", ""), "isTriggered": "y"}
        logger.info(f"gibberish_log={gibberish_log}")
                
        session_tools.update_sub_state('UNRECOGNIZED-INTENT-MENU-STATE')
        return render_spiels_options(session_attributes=event)
    else: 
        session_utils.increase_global_retry_count(session_tools = session_tools)
        gibberish_log = {"flow": "validate concern no", "lob": "na", "message": event.get("message", ""), "psid": event.get("fbId", "")}
        logger.info(f"gibberish_log={gibberish_log}")
        
        res.send_message(sender_id, UNRECOGNIZED_NUMBER_FORMAT_SPIEL)
        return res.send_message(sender_id, GET_ALL_LOB_NUMBER_SPIEL_GUIDELINES_2)



def validate_number_lob(number): 
    subscriber = subscriber_utils.get_concern_no_subscriber_details(number)
    logger.info(f"Number: {number} Subscriber Exist: {subscriber.is_subscriber_exists()} Subscriber LOB: {subscriber.get_lob_name()}")
    if subscriber.is_subscriber_exists() and subscriber.get_lob_name() == constants.UKNOWN_LOB_NAME:
        #Not in DB
        common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1423", cj=cj)

        session_tools.update_session_context_attributes({"concernNumberConfirmation": "true"})
        session_tools.update_last_brand(subscriber.get_lob_name())

        handle_number_not_existing()
        res.send_quickresponse(
            sender_id, CONFIRM_NUMBER_CONCERN_SPIEL_1, YES_NO_MENU, MENU_FORM)
        return {
            "isValidated": True,
            "number": number,
            "subscriberLob": "",
            "isExisting": False,
            "isValidLob": False
        }      
    else:
        common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1422", cj=cj)

        if not subscriber.get_lob_name() in lob_list: 
            #Invalid lob combi for intent
            common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1431", cj=cj)
    
            session_tools.update_sub_state('UNRECOGNIZED-INTENT-MENU-STATE')
            session_tools.update_last_brand(subscriber.get_lob_name())

            res.send_message(sender_id, UNRECOGNIZED_NUMBER_LOB_SPIEL)
            render_spiels_options(session_attributes=event) 
            common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1432", cj=cj)
            return {
                "isValidated": True,
                "number": number,
                "subscriberLob": subscriber.get_lob_name(),
                "isExisting": True,
                "isValidLob": False
            }
        else:
            #valid lob
            common_session_utils.append_cj(brand=session_tools.get_last_brand(), flow="1430", cj=cj)
            session_tools.update_attributes({"unrecognizedRetry": "0"})
            return {
                "isValidated": True,
                "number": number,
                "subscriberLob": subscriber.get_lob_name(),
                "isExisting": True,
                "isValidLob": True
            }
