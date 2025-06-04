
import logging  
 
from helpers.customerjourneytools import CustomerJourney
from helpers.sessiontools import SessionTools
from helpers.subscribertools import SubscriberTools
from helpers.common.helpers.session_context import SessionContext

import resources.constants as constants
import resources.tableattributes as tableattributes

logger = logging.getLogger()
logger.setLevel(logging.INFO)

cj: CustomerJourney
session_tools: SessionTools

def append_cj(**kwargs) -> None:
    brand = kwargs.get("brand", None)
    flow = kwargs.get("flow", None)
    cj = kwargs.get("cj", None)
    
    if not flow:
        logger.info('Flow is required')
        return
    
    if (not cj) or not isinstance(cj, CustomerJourney):
        logger.info('cj:CustomerJourney is required')
        return

    cj.append_journey(cj.get_journey_id(flow=flow, brand=brand))
	
	
def is_retry_maxed(session_tools, limit: int) -> bool:
    retry = int(session_tools.get_retry()) + 1

    if retry > limit:
        session_tools.reset_retry()
        return True

    session_tools.update_retry(retry)
    return False


def save_subscriber_details(ctx: SessionContext, **kwargs) -> None:

    subscriber: SubscriberTools = kwargs.get("subscriber", None)
    lob_name = subscriber.get_lob_name()
    sg_lob = subscriber.get_sg_lob()

    if lob_name == constants.BB_LOB_NAME:
        brand_type = "wireline"
    elif lob_name == constants.BUSINESS_SG_LOB_NAME and sg_lob.upper() == "BROADBAND":
        brand_type = "wireline"
    else:
        brand_type = "wireless"

    ctx.session_tools.update_attributes({
        tableattributes.LAST_NUMBER: subscriber.get_msisdn(),
        tableattributes.LAST_BRAND: subscriber.get_lob_name(),
        tableattributes.LAST_LANDLINE: subscriber.get_landline(),
        tableattributes.LAST_SG_BRAND: subscriber.get_sg_lob(),
        tableattributes.LAST_ACCOUNT_NUMBER: subscriber.get_account_no(),
        tableattributes.LAST_BSS_CONTACT_ID: subscriber.get_bss_contact_id(),
        tableattributes.IS_SENIOR: subscriber.is_senior(),
        tableattributes.LAST_MSISDN: subscriber.get_msisdn(),
        tableattributes.BRAND_TYPE: brand_type
    })