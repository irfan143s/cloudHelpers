from __future__ import annotations

import boto3
import json
import logging

import helpers.utils as utils
import resources.aws_lambda as lmb_functions

from resources.common.enums.cx_channels import CxChannels
from resources.common.enums.cx_agent_platforms import CxAgentPlatforms

import configuration as configs


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def invoke_transfer_to_agent(**kwargs) -> bool:
    logger.info(f"common:invoke_transfer_to_agent() kwargs={kwargs}")

    lmbd_clnt_oregon = boto3.client("lambda", region_name = configs.REGION_OREGON)
    cx_channels = [channel for channel in CxChannels]
    cx_agent_platforms = [cx_agent_platform for cx_agent_platform in CxAgentPlatforms]

    request = kwargs.get("request", {})
    cx_channel = kwargs.get("cx_channel", None)
    cx_agent_platform = kwargs.get("cx_agent_platform", None)
    intent_id = kwargs.get("intent_id", "")
    intent_queue_id = kwargs.get("intent_queue_id", "")
    support_intent = kwargs.get("support_intent", "")
    spiel = kwargs.get("spiel", "")
    meta_data = kwargs.get("meta_data", {})

    if not isinstance(request, dict):
        logger.info(f"common:invoke_transfer_to_agent() -> request:dict is required.")
        return False

    if not cx_agent_platform or cx_agent_platform not in cx_agent_platforms:
        logger.info(f"common:invoke_transfer_to_agent() -> cx_agent_platform:CxAgentPlatforms is required.")
        return False

    if not cx_channel or cx_channel not in cx_channels:
        logger.info(f"common:invoke_transfer_to_agent() -> channel:CxChannel is required.")
        return False

    if spiel and not isinstance(spiel, str):
        logger.info(f"common:invoke_transfer_to_agent() -> spiel:str is required.")
        return False
    
    if meta_data and not isinstance(meta_data, dict):
        logger.info(f"common:invoke_transfer_to_agent() -> meta_data:dict is required.")
        return False

    if cx_agent_platform == CxAgentPlatforms.CONNECT:
        if not intent_queue_id:
            logger.info(f"common:invoke_transfer_to_agent() -> intent_queue_id is required for CONNECT agent platform.")
            return False
    elif cx_agent_platform == CxAgentPlatforms.LIVE_PERSON:
        if not support_intent:
            logger.info(f"common:invoke_transfer_to_agent() -> support_intent is required for LIVE PERSON agent platform.")
            return False
    else:
        if not intent_id:
            logger.info(f"common:invoke_transfer_to_agent() -> intent_id is required for SOCIO agent platform.")
            return False
        

    request['cxChannel'] = cx_channel.value
    request['cxAgentPlatform'] = cx_agent_platform.value
    request['intentId'] = intent_id
    request['supportIntent'] = support_intent
    request['intentQueueId'] = intent_queue_id
    request['connectToAgentSpiel'] = spiel
    request['intentMetadata'] = meta_data

    try:
        transfer_to_agent_response = lmbd_clnt_oregon.invoke(FunctionName = lmb_functions.TRANSFER_TO_AGENT_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))
        logger.info(f"transferToAgent response: {transfer_to_agent_response}")
    except Exception as error:
        logger.info(f"Error invoking {lmb_functions.TRANSFER_TO_AGENT_LAMBDA}: {utils.get_exception_str(error)}")
        return False

    return True


def transfer_to_socio_agent(**kwargs) -> bool:
     
    request = kwargs.get("request", {})
    intent_id = kwargs.get("intent_id", "")
    meta_data = kwargs.get("meta_data", {})
    spiel = kwargs.get("spiel", "")

    if invoke_transfer_to_agent(request=request, cx_agent_platform=CxAgentPlatforms.SOCIO, cx_channel=CxChannels.FACEBOOK, intent_id=intent_id, meta_data=meta_data, spiel=spiel):
        return True
    return False


def transfer_to_live_person_agent(**kwargs) -> bool:
    
    request = kwargs.get("request", {})
    support_intent = kwargs.get("support_intent", "")
    meta_data = kwargs.get("meta_data", {})
    spiel = kwargs.get("spiel", "")

    if invoke_transfer_to_agent(request=request, cx_agent_platform=CxAgentPlatforms.LIVE_PERSON, cx_channel=CxChannels.FACEBOOK, support_intent=support_intent, meta_data=meta_data, spiel=spiel):
        return True
    return False


def transfer_to_conenct_agent(**kwargs) -> bool:
    return True
