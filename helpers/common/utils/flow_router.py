import boto3
import json
import logging

from helpers.common.helpers.session_context import SessionContext
import helpers.utils as utils

import resources.aws_lambda as aws_lambdas
import resources.states as states

import configuration as configs

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _invoke_lambda_function(**kwargs) -> None:
    request = kwargs.get("request", {})
    lambda_function = kwargs.get("lambda_function", "")
    lmbd_clnt_oregon = boto3.client("lambda", region_name=configs.REGION_OREGON)

    try:
        lmbd_clnt_oregon.invoke(FunctionName=lambda_function, InvocationType="Event", Payload=json.dumps(request))
    except Exception as error:
        logger.error(f"Failed to invoke: {lambda_function} due to: {utils.get_exception_str(error)}")
    

def route_to_network_mobile_roaming(ctx: SessionContext) -> None:
    logger.info(f"Routing to network mobile roaming...")

    custom_attr = {
        "sessionState": states.NETWORK_CONCERN_MOBILE_STATE,
        "subState": "route-to-network-mobile-roaming"
    }

    ctx.session_tools.update_attributes(custom_attr)
    ctx.request.update(custom_attr)
    _invoke_lambda_function(request=ctx.request, lambda_function=aws_lambdas.NETWORK_CONCERN_LAMBDA)


def route_to_network_lob_check(ctx: SessionContext, subscriber_no: str) -> None:
    logger.info(f"Routing to network lob check...")

    custom_attr = {
        "sessionState": states.NETWORK_CONCERN_MOBILE_STATE,
        "subState": "route-to-lob-check"
    }
    ctx.session_tools.update_attributes(custom_attr)

    custom_attr.update({
        "message": subscriber_no
    })
    ctx.request.update(custom_attr)
    _invoke_lambda_function(request=ctx.request, lambda_function=aws_lambdas.NETWORK_CONCERN_LAMBDA)


def route_to_gcash_platinum(fbId, fbName, registeredNumber, subState, message = "") -> None:
    logger.info(f"Routing to gcashPlatinum flow...")
    custom_attr = {
        "fbId": fbId,
        "channel": configs.THEA_PAGE_ID,
        "firstName": fbName,
        "msisdn": registeredNumber,
        "registeredNumber": registeredNumber,
        "notification": '1',
        "sessionState": states.THEA_GCASH_PLATINUM_STATE,
        "subState": subState,
        "message": message 
    }
    _invoke_lambda_function(request=custom_attr, lambda_function=aws_lambdas.THEA_GCASH_PLATINUM_LAMBDA)
