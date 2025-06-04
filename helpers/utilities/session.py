from __future__ import annotations

import boto3
import json

from helpers.sessiontools import SessionTools
from helpers.subscribertools import SubscriberTools
from helpers.customerjourneytools import CustomerJourney

import resources.tableattributes as tbl_attrs
import resources.aws_lambda as lambda_func
import resources.constants as constants

import configuration as config


def append_cj(sender_id:str, channel_id:str, flow_id:str) -> None:
    cj = CustomerJourney(sender_id, channel_id)
    cj.append_journey(cj.get_journey_id(flow=flow_id))


def update_state(session_tools:SessionTools, session_state:str) -> None:
    if session_tools.get_state() !=  session_state:
        session_tools.update_state(session_state)


def update_sub_state(session_tools:SessionTools, sub_state:str) -> None:
    if session_tools.get_sub_state() !=  sub_state:
        session_tools.update_sub_state(sub_state)


def save_subscriber_details(session_tools: SessionTools, subscriber: SubscriberTools) -> None:
    
    lob_name = subscriber.get_lob_name()
    sg_lob = subscriber.get_sg_lob()

    if lob_name == constants.BB_LOB_NAME:
        brand_type = "wireline"
    elif lob_name == constants.BUSINESS_SG_LOB_NAME and sg_lob.upper() == "BROADBAND":
        brand_type = "wireline"
    else:
        brand_type = "wireless"

    session_tools.update_attributes({
        tbl_attrs.LAST_NUMBER: subscriber.get_msisdn(),
        tbl_attrs.LAST_BRAND: subscriber.get_lob_name(),
        tbl_attrs.LAST_LANDLINE: subscriber.get_landline(),
        tbl_attrs.LAST_SG_BRAND: subscriber.get_sg_lob(),
        tbl_attrs.LAST_ACCOUNT_NUMBER: subscriber.get_account_no(),
        tbl_attrs.LAST_BSS_CONTACT_ID: subscriber.get_bss_contact_id(),
        tbl_attrs.IS_SENIOR: subscriber.is_senior(),
        tbl_attrs.LAST_MSISDN: subscriber.get_msisdn(),
        tbl_attrs.BRAND_TYPE: brand_type,
        "lastCustomerType": subscriber.get_customer_type()
    })


def get_global_retry_count(session_tools: SessionTools, **kwargs):
    return session_tools.get_global_retry_count() + 1


def increase_global_retry_count(session_tools: SessionTools, **kwargs) -> None:
    global_retry_count = session_tools.get_global_retry_count() + 1
    session_tools.update_global_retry_count(global_retry_count)


def is_global_retry_count_reached_threshold(session_tools: SessionTools, **kwargs):
    global_retry_count = session_tools.get_global_retry_count() + 1

    if global_retry_count >= config.GLOBAL_RETRY_THRESHOLD:
        return True
    
    return False

