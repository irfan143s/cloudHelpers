import boto3
import json
import logging

import helpers.utils as utils

from resources.common.enums.cx_channels import CxChannels
from resources.common.enums.cx_agent_platforms import CxAgentPlatforms

import helpers.common.utils.flow as common_flow_utils

from helpers.sessiontools import SessionTools

from resources.aws_lambda import (
    THEA_MENU_LAMBDA,
    TRANSFER_TO_AGENT_LAMBDA,
    FOLLOWUP_LAMBDA,
    MAIN_MENU_LAMBDA,
    BILLS_AND_PAYMENTS_LAMBDA,
    LOSTPHONE_OR_SIM_LAMBDA,
    MODIFY_OR_TERMINATE_LAMBDA,
    REF_LINK_FLOW_LAMBDA,
    RECONNECT_MY_LINE_LAMBDA,
    NETWORK_CONCERN_LAMBDA,
    LOAD_PROMOS_AND_REWARDS_LAMBDA,
    PROACTIVE_RENEWAL_LAMBDA,
    FOLLOWUP_CONCERN_LAMBDA,
    CUSTOMER_VERIFICATION_LAMBDA
)
from resources.states import (
    MAIN_MENU_STATE,
    BILLS_AND_PAYMENTS_STATE,
    LOSTPHONE_OR_SIM_STATE,
    MODIFY_OR_TERMINATE_STATE,
    MODIFY_OR_TERMINATE_BB_UPGRADE_PLAN_STATE,
    RECONNECT_MY_LINE_STATE,
    NETWORK_CONCERN_STATE,
    THEA_REGISTRATION_STATE,
    EXIT_PLATINUM_UPGRADE_STATE,
    UNREFLECTED_BILL_STATE,
    LOAD_PROMOS_AND_REWARDS_STATE,
    PROACTIVE_RENEWAL_STATE,
    UNKNOWN_CHARGES_STATE,
    FOLLOWUP_CONCERN_STATE,
    CUSTOMER_VERIFICATION_STATE
)
from resources.resourcemapping import (
    state_default_sub_state_mapping_dict
)
from resources.spiels import(
    THEA_CONNECT_TO_AN_AGENT_SPIEL,
    CONNECT_TO_AN_AGENT_V3_SPIEL
)
import resources.tableattributes as tableattributes

from resources.api import *
from resources import constants
from resources import intentkeys

from configuration import (
    REGION_OREGON,
    socioBasket,
    CONNECT_CHAT_INTENT_QUEUE_IDS,
    THEA_PAGE_ID
)


logger = logging.getLogger()
logger.setLevel(logging.INFO)
    

"""****************************************************************************************
*************** Put transferring flow methods here used on multiple places ****************
****************************************************************************************"""

def invoke_transfer_to_agent(request, intent_id, meta_data={}, connect_to_agent_spiel=None):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)

    transfer_to_agent_payload = request
    transfer_to_agent_payload['intentId'] = intent_id
    transfer_to_agent_payload['intentMetadata'] = meta_data
    transfer_to_agent_payload['connectToAgentSpiel'] = connect_to_agent_spiel

    try:
        transfer_to_agent_response = lmbd_clnt_oregon.invoke(FunctionName = TRANSFER_TO_AGENT_LAMBDA, InvocationType = "Event", Payload = json.dumps(transfer_to_agent_payload))
        # transfer_to_agent_response = json.loads(transfer_to_agent_response['Payload'].read().decode())
        logger.info(f"transferToAgent response: {transfer_to_agent_response}")
    except Exception as error:
        logger.info(f"Error invoking {TRANSFER_TO_AGENT_LAMBDA}: {utils.get_exception_str(error)}")
        return False

    return True

    # if  transfer_to_agent_response['statusCode'] != 200:
    #     return False
    # else:
    #     return True


def transfer_to_connect_agent(**kwargs):
    request = kwargs.get("request", {})
    intent_queue_id = kwargs.get("intent_queue_id", "")
    meta_data = kwargs.get("meta_data", {})
    spiel =  kwargs.get("spiel", "")
    fb_name = request.get("fbName", "no-name")


    meta_data.update({
        "fbName": fb_name,
        "intentQueueId": intent_queue_id
    })

    transfer_result = common_flow_utils.invoke_transfer_to_agent(
            request=request,
            cx_channel=CxChannels.FACEBOOK,
            cx_agent_platform=CxAgentPlatforms.CONNECT,
            intent_queue_id=intent_queue_id,
            meta_data=meta_data,
            spiel = spiel
    )

    if transfer_result:
        return True
    return False

def thea_transfer_to_connect_agent(**kwargs):
    request = kwargs.get("request", {})
    intent = kwargs.get("intent", "")
    fb_name = request.get("fbName", "no-name")
    registered_number = request.get("registeredNumber", "")
    intent_queue_id = CONNECT_CHAT_INTENT_QUEUE_IDS[THEA_PAGE_ID].get(intent, "")
    spiel = kwargs.get("spiel", THEA_CONNECT_TO_AN_AGENT_SPIEL)

    meta_data ={
        "fbName": fb_name,
        "intentQueueId": intent_queue_id,
        "registeredNumber": registered_number
    }

    transfer_result = common_flow_utils.invoke_transfer_to_agent(
            request=request,
            cx_channel=CxChannels.FACEBOOK,
            cx_agent_platform=CxAgentPlatforms.CONNECT,
            intent_queue_id=intent_queue_id,
            meta_data=meta_data,
            spiel = spiel
    )

    if transfer_result:
        return True
    return False


def route_to_followup(request):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request['subState'] = "0"
    try:
        lmbd_clnt_oregon.invoke(FunctionName = FOLLOWUP_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {FOLLOWUP_LAMBDA} due to: {utils.get_exception_str(error)}")


def route_to_main_menu(request, session_tools):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "subState": "0",
        "sessionState": MAIN_MENU_STATE
    })
    session_tools.reset_state()
    session_tools.update_attributes({"sessionState": MAIN_MENU_STATE, "subState": "0"})
    try:    
        lmbd_clnt_oregon.invoke(FunctionName = MAIN_MENU_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {MAIN_MENU_LAMBDA} due to: {utils.get_exception_str(error)}")


def route_to_bills_and_payments_bill_inquiry(request, request_attrs={}):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "sessionState": UNKNOWN_CHARGES_STATE,
        "subState":  "GET-DISPUTE-DETAILS"
    })
    request.update(request_attrs)
    try:
        lmbd_clnt_oregon.invoke(FunctionName = BILLS_AND_PAYMENTS_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {BILLS_AND_PAYMENTS_LAMBDA} due to: {utils.get_exception_str(error)}")


def route_to_bills_and_payments(request, request_attrs={}):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "sessionState": BILLS_AND_PAYMENTS_STATE,
        "subState":  state_default_sub_state_mapping_dict[BILLS_AND_PAYMENTS_STATE]
    })
    request.update(request_attrs)
    try:
        lmbd_clnt_oregon.invoke(FunctionName = BILLS_AND_PAYMENTS_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {BILLS_AND_PAYMENTS_LAMBDA} due to: {utils.get_exception_str(error)}")
    
def route_to_bills_and_payments_bill_not_reflected(request, request_attrs={}):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "sessionState": UNREFLECTED_BILL_STATE,
        "subState":  state_default_sub_state_mapping_dict[UNREFLECTED_BILL_STATE]
    })
    request.update(request_attrs)
    try:
        lmbd_clnt_oregon.invoke(FunctionName = BILLS_AND_PAYMENTS_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {BILLS_AND_PAYMENTS_LAMBDA} due to: {utils.get_exception_str(error)}")

def route_to_load_promos_and_rewards(request, request_attrs={}):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "sessionState": LOAD_PROMOS_AND_REWARDS_STATE,
        "subState":  state_default_sub_state_mapping_dict[LOAD_PROMOS_AND_REWARDS_STATE]
    })
    request.update(request_attrs)
    try:
        lmbd_clnt_oregon.invoke(FunctionName = LOAD_PROMOS_AND_REWARDS_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {LOAD_PROMOS_AND_REWARDS_LAMBDA} due to: {utils.get_exception_str(error)}")


def route_to_lost_phone_or_sim(request, request_attrs={}):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "sessionState": LOSTPHONE_OR_SIM_STATE,
        "subState":  "DPN"
    })
    request.update(request_attrs)
    try:
        lmbd_clnt_oregon.invoke(FunctionName = LOSTPHONE_OR_SIM_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {LOSTPHONE_OR_SIM_LAMBDA} due to: {utils.get_exception_str(error)}")


def route_to_wireline_upgrade_plan(request, request_attrs={}):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "sessionState": MODIFY_OR_TERMINATE_BB_UPGRADE_PLAN_STATE,
        "subState":  "0"
    })
    request.update(request_attrs)
    try:
        lmbd_clnt_oregon.invoke(FunctionName = MODIFY_OR_TERMINATE_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {MODIFY_OR_TERMINATE_LAMBDA} due to: {utils.get_exception_str(error)}")

def route_to_modify_or_terminate(request, request_attrs={}):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "sessionState": MODIFY_OR_TERMINATE_STATE,
        "subState":  "0"
    })
    request.update(request_attrs)
    try:
        lmbd_clnt_oregon.invoke(FunctionName = MODIFY_OR_TERMINATE_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {MODIFY_OR_TERMINATE_LAMBDA} due to: {utils.get_exception_str(error)}")

def route_to_wireless_change_plan(request, request_attrs={}):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "sessionState": MODIFY_OR_TERMINATE_STATE,
        "subState":  "3",
        "menuId": "[menu].iwanttochangemyplan"
    })
    request.update(request_attrs)
    try:
        lmbd_clnt_oregon.invoke(FunctionName = MODIFY_OR_TERMINATE_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {MODIFY_OR_TERMINATE_LAMBDA} due to: {utils.get_exception_str(error)}")


def route_to_reflink_flow(request, request_attrs={}):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "sessionState": "INIT",
        "subState":  "INIT"
    })
    request.update(request_attrs)
    try:
        lmbd_clnt_oregon.invoke(FunctionName = REF_LINK_FLOW_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {REF_LINK_FLOW_LAMBDA} due to: {utils.get_exception_str(error)}")


def route_to_reconnect_my_line(request, request_attrs={}):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "sessionState": RECONNECT_MY_LINE_STATE,
        "subState":  "DPN"
    })
    request.update(request_attrs)
    try:
        lmbd_clnt_oregon.invoke(FunctionName = RECONNECT_MY_LINE_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {RECONNECT_MY_LINE_LAMBDA} due to: {utils.get_exception_str(error)}")


def route_to_network_concern(session_tools: SessionTools, request, request_attrs=None):
    logger.info(f"Routing to network concern main...")
    
    if request_attrs == None:
        request_attrs = {}

    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)

    session_tools.update_attributes({tableattributes.DPN_STATE: "0"})

    request.update({
        tableattributes.SESSION_STATE: NETWORK_CONCERN_STATE,
        tableattributes.SUB_STATE:  "DPN"
    })
    request.update(request_attrs)
    
    try:
        lmbd_clnt_oregon.invoke(FunctionName = NETWORK_CONCERN_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {NETWORK_CONCERN_LAMBDA} due to: {utils.get_exception_str(error)}")

def route_to_network_concern_skip_dpn(session_tools: SessionTools, request, request_attrs=None):
    route_to_network_concern(session_tools, request, {"subState":"0"})

"""
    x_attributes = custom attributes
"""
def route_to_followup_concern(**kwargs) -> None:
    x_attributes = kwargs.get("x_attributes", {})
    request = kwargs.get("request", {})

    request.update({
        tableattributes.SESSION_STATE: FOLLOWUP_CONCERN_STATE,
        tableattributes.SUB_STATE: state_default_sub_state_mapping_dict[FOLLOWUP_CONCERN_STATE]
    })
    request.update(x_attributes)

    try:
        lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
        lmbd_clnt_oregon.invoke(FunctionName = FOLLOWUP_CONCERN_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {FOLLOWUP_CONCERN_LAMBDA} due to: {utils.get_exception_str(error)}")


def route_to_roaming(request, request_attrs={}):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "sessionState": NETWORK_CONCERN_STATE,
        "subState":  "CHECK-MOBILE",
        "menuId": "[menu].roaming",
        "message": "[menu].roaming"
    })
    request.update(request_attrs)
    try:
        lmbd_clnt_oregon.invoke(FunctionName = NETWORK_CONCERN_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {NETWORK_CONCERN_LAMBDA} due to: {utils.get_exception_str(error)}")


def route_to_thea_registration(session_tools: SessionTools, request, request_attrs=None):
    logger.info(f"Routing to Thea registration...")
    if request_attrs == None:
        request_attrs = {}

    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)

    session_tools.update_attributes({
        tableattributes.SESSION_STATE: THEA_REGISTRATION_STATE,
        tableattributes.SUB_STATE:  "DPN"
    })

    request.update({
        tableattributes.SESSION_STATE: THEA_REGISTRATION_STATE,
        tableattributes.SUB_STATE:  "DPN"
    })
    request.update(request_attrs)

    try:
        lmbd_clnt_oregon.invoke(FunctionName = THEA_MENU_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {THEA_MENU_LAMBDA} due to: {utils.get_exception_str(error)}")

def route_to_lambda_dynamic(request, lambda_name, request_attrs={}):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)

    request.update(request_attrs)
    try:
        lmbd_clnt_oregon.invoke(FunctionName = lambda_name, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {lambda_name} due to: {utils.get_exception_str(error)}")
        return False
    
    return True


def transfer_senior_to_an_agent(**kwargs):
    logger.info(f"Subscriber is a senior. kwargs: {kwargs}")
    if not "request" in kwargs.keys() or not kwargs["request"]:
        logger.error("request is required on transfer_senior_to_an_agent()")
        return

    request = kwargs["request"]
    brand = kwargs.get("brand", "")
    sb_brand = kwargs.get("sg_brand", "").upper().strip() 
    intent_key = intentkeys.SENIOR_POSTPAID
    support_intent = 'senior-postpaid'

    if not brand or brand not in constants.ACCOUNT_BRANDS:
        intent_key = intentkeys.SENIOR_POSTPAID
        support_intent = 'senior-postpaid'

    if brand in [constants.PLATINUM_MOBIE_LOB_NAME, constants.PLATINUM_BB_LOB_NAME]:
        intent_key = intentkeys.FB_VIP
    elif brand in constants.POSTPAID_ACCOUNT_BRANDS:
        intent_key = intentkeys.SENIOR_POSTPAID
        support_intent = 'senior-postpaid'
    elif brand in constants.BROADBAND_ACCOUNT_BRANDS:
        intent_key = intentkeys.SENIOR_BROADBAND
        support_intent = 'senior-broadband'
    elif brand == constants.BUSINESS_SG_LOB_NAME:
        if not sb_brand:
            intent_key = intentkeys.SENIOR_POSTPAID
        else:
            if sb_brand == "POSTPAID":
                intent_key = intentkeys.SENIOR_POSTPAID
            elif sb_brand == "BROADBAND":
                intent_key = intentkeys.SENIOR_BROADBAND

    intent_id = socioBasket[request['channel']][intent_key]
    if support_intent:
        common_flow_utils.transfer_to_live_person_agent(request = request, support_intent = support_intent, spiel = CONNECT_TO_AN_AGENT_V3_SPIEL)
    else:
        invoke_transfer_to_agent(request, intent_id, {}, CONNECT_TO_AN_AGENT_V3_SPIEL)
    

def route_to_thea_main_menu(request, request_attrs={}):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "sessionState": EXIT_PLATINUM_UPGRADE_STATE,
        "subState":  "0"
    })
    request.update(request_attrs)
    try:
        lmbd_clnt_oregon.invoke(FunctionName = THEA_MENU_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {THEA_MENU_LAMBDA} due to: {utils.get_exception_str(error)}")

def route_to_thea_otp_menu(request, request_attrs={}):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "sessionState": THEA_REGISTRATION_STATE,
        "subState":  "MENU-OTP",
        "otpReferrer":  "PLATINUM-UPGRADE-REFLINK"
    })
    request.update(request_attrs)
    try:
        lmbd_clnt_oregon.invoke(FunctionName = THEA_MENU_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {THEA_MENU_LAMBDA} due to: {utils.get_exception_str(error)}")
    
def route_to_customer_verification(session_tools: SessionTools, request, request_attrs={}):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)

    session_tools.update_session_context_attributes({
        'lastSessionState': session_tools.get_state(),
        'lastSubState':  session_tools.get_sub_state(),
        'lastMessage': request.get("message", ""),
        'lastUserInput': session_tools.get_user_input()
    })

    request.update({
        "sessionState": CUSTOMER_VERIFICATION_STATE,
        "subState":  "INIT"
    })
    request.update(request_attrs)
    try:
        lmbd_clnt_oregon.invoke(FunctionName = CUSTOMER_VERIFICATION_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {CUSTOMER_VERIFICATION_LAMBDA} due to: {utils.get_exception_str(error)}")