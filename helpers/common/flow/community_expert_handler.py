from datetime import datetime

from configuration import *
from resources.spiels import *
from resources.constants import *
from helpers.resFormatter import ResFormatter
from helpers.utils import get_current_time

import helpers.common.utils.flow as common_utils_flow
import helpers.utilities.subscriber as subscriber_utilities
import helpers.whitelistchecker as whitelistchecker
import helpers.utilities.subscriber as subscriber_utils


import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def community_expert_handler(**kwargs):
    init(**kwargs)
    request = kwargs.get("request", {})

    return execute_coex_whitelisted_handling(request=request)


def init(**kwargs):
    global sender_id, page_id, lob_name, msisdn, account_no, subscriber
    global res_formatter

    request = kwargs.get("request", {})
    sender_id = request.get("fbId", "")
    page_id = request.get("channel", "")

    res_formatter = ResFormatter(page_id)

def execute_coex_whitelisted_handling(**kwargs):
    request = kwargs.get("request", {})
    message = request.get("message", "")
    
    if not is_within_hoop():
        return False

    subscriber = subscriber_utils.get_concern_no_subscriber_details(message)
    lob_name = subscriber.get_lob_name()
    msisdn = subscriber.get_msisdn()
    account_no = subscriber.get_account_no()
    is_coex_whitelisted = False

    if not subscriber.is_subscriber_exists() and subscriber.get_lob_name() != constants.UKNOWN_LOB_NAME:
        logger.info(f"subs does not exists or it's unknown")
        return False
    
    if account_no:
        logger.info(f"Checking if sub is coex whitelisted using accountNo: {account_no}")
        is_coex_whitelisted = whitelistchecker.is_coex_whitelisted_by_account_no(account_no)
        
    if not is_coex_whitelisted:
        logger.info(f"Checking if sub is coex whitelisted using msisdn: {msisdn}")
        is_coex_whitelisted = whitelistchecker.is_coex_whitelisted_by_msisdn(msisdn)

    if not is_coex_whitelisted:
        logger.info(f"sub is not coex whitelisted")
        return False

    if not is_valid_lob(lob_name):
        logger.info(f"sub doesnt have valid lob: {lob_name}")
        return False

    logger.info(f"sub has valid lob: {lob_name}")
    handle_coex_prechecks(request = request, account_no = account_no, msisdn = msisdn)
    transfer_to_live_person_agent(request = request)
    return True

def is_valid_lob(lob_name):

    if lob_name not in [ POSTPAID_LOB_NAME, BB_LOB_NAME, PREPAID_LOB_NAME, TM_LOB_NAME]:
        return False

    return True

def handle_coex_prechecks(**kwargs):
    request = kwargs.get("request", {})
    msisdn = kwargs.get("msisdn", {})
    account_no = kwargs.get("account_no", {})
    logger.info(f"handling coex whitelist prechecks")

    customer_info = {}
    is_outage = False
    if account_no:
        customer_info = subscriber_utilities.get_customer_info(account_no=account_no)
        is_outage = subscriber_utilities.is_outage(account_no=account_no)
    else:
        customer_info = subscriber_utilities.get_customer_info(msisdn=msisdn)
        
    subscriber_status = customer_info.get("subscriber_status", "")

    if subscriber_status != "65":
        logger.info(f"Subscriber is NOT ACTIVE with subscriber status of {subscriber_status}.")

        if subscriber_status in ["83", "68"]:
            logger.info(f"Sub is TD")
            res_formatter.send_message(sender_id, COEX_SUB_INITIATED_TD_SPIEL)
        if subscriber_status in ["67", "84", "76"]:
            logger.info(f"Sub is PD")
            res_formatter.send_message(sender_id, COEX_SUB_INITIATED_PD_SPIEL)
        if subscriber_status in ["85"]:
            logger.info(f"Sub is TD due to OB")
            res_formatter.send_message(sender_id, COEX_OB_TD_SPIEL)

    if is_outage:
        logger.info(f"Sub is part of Outage")
        res_formatter.send_message(sender_id, COEX_PART_OF_BB_OUTAGE_SPIEL)

    return

def is_within_hoop():
    current_datetime_str = get_current_time()
    current_datetime = datetime.fromisoformat(current_datetime_str)
    current_time = current_datetime.time()
    coex_hoop_start = datetime.strptime(COEX_HOOP_START, "%H:%M:%S").time()
    coex_hoop_end = datetime.strptime(COEX_HOOP_END, "%H:%M:%S").time()

    if not (coex_hoop_start <= current_time <= coex_hoop_end ):
        return False

    return True

def transfer_to_live_person_agent(**kwargs):
    request = kwargs.get("request", {})
    logger.info(f"transferring to agent for coex whitelist")
    return common_utils_flow.transfer_to_live_person_agent(request = request, support_intent = "community-experts")
