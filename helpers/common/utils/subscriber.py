
import logging

from helpers.subscribertools import SubscriberTools

import helpers.common.utils.formatter as formatter_utils
import helpers.common.utils.validation as validation_utils
import resources.common.constants.str as str_const
import resources.constants as constants
import resources.common.constants.str as str_const

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_subsriber_status_value(**kwargs):
    status = kwargs.get("status", "")

    status_value_map = {
        "65": str_const.ACTIVE,
        "67": str_const.PD_DUE_TO_CANCELLATION,
        "83": str_const.TD_DUE_TO_SUSPENSION,
        "85": str_const.TD_DUE_TO_COLLECTION_SUSPENSION,
        "68": str_const.TD_DUE_TO_VOLUNTARY_SUSPENSION,
        "84": str_const.PD_DUE_TO_CHANGE_OWNERSHIP,
        "76": str_const.PD_DUE_TO_COLLECTION_CANCELLATION
    }
    
    return status_value_map.get(status, str_const.ACTIVE)


def get_subsriber_status(**kwargs):
    status = kwargs.get("status", "")

    status_map = {
        "65": str_const.ACTIVE,
        "67": str_const.PD,
        "83": str_const.TD,
        "85": str_const.TD,
        "68": str_const.TD,
        "84": str_const.PD,
        "76": str_const.PD
    }

    return status_map.get(status, str_const.ACTIVE)


def get_subscriber_by_mobile_no(mobile_no) -> SubscriberTools:
    mobile_no = formatter_utils.to_13_digits_ph_mobile_no(mobile_no)
    return SubscriberTools("MSISDN", mobile_no)


def get_subscriber_by_mobile_or_account_no(concern_no) -> SubscriberTools:
    if validation_utils.is_valid_ph_mobile_number(concern_no):
        formatted_concern_no = formatter_utils.to_13_digits_ph_mobile_no(concern_no)
        subscriber = SubscriberTools("MSISDN", formatted_concern_no)
        if subscriber.is_subscriber_exists():
            return subscriber

    subscriber = SubscriberTools("ACCOUNTNUMBER", concern_no)
    if subscriber.is_subscriber_exists():
        return subscriber
        
    return None


def get_brand_type(**kwargs) -> str:
    last_brand = kwargs.get("last_brand", "")
    last_sg_brand = kwargs.get("last_sg_brand", "")

    if last_brand == constants.BB_LOB_NAME:
        brand_type = str_const.WIRELINE
    elif last_brand == constants.BUSINESS_SG_LOB_NAME and last_sg_brand.upper() == "BROADBAND":
        brand_type = str_const.WIRELINE
    else:
        brand_type = str_const.WIRELESS

    return brand_type

